import os
from data.kaeyastats import Kaeya
from data.swords import initialize_swords
from data.artifacts import initialize_artifacts

# Average ATK% per ATK% substat roll.
N_A = 0.04975
# Average CR per CR substat roll.
N_CR = 0.033
# Average CD per CD substat roll.
N_CD = 0.066


def brute_force_substat_optimizer(B, O, F, OR, OD, N, sword_name):
    # Reference:
    # The probability of all 25 substat rolls going into ATK% or CD or CR is: 0.75^25 = 0.0752%
    # The probability of at least 20 rolls going into ATK% or CD or CR is: 0.75^25+...+0.75^20 = 1.042%
    # The probability of at least 15 rolls going into ATK% or CD or CR is: 0.75^25+...+0.75^15 = 5.119%
    # The probability of at least 10 rolls going into ATK% or CD or CR is: 0.75^25+...+0.75^10 = 22.29%
    # The probability of at least 5 rolls going into ATK% or CD or CR is: 0.75^25+...+0.75^5 = 94.69%

    max_D = -1
    max_A_roll = 0
    max_CR_roll = 0
    max_CD_roll = N
    for i in range(0, N+1):
        for j in range(0, N+1-i):
            k = N - i - j

            A = i * N_A
            CR = j * N_CR
            CD = k * N_CD
            D = (B * (1.0 + A + O) + F) * (1.0 + (CR + OR) * (CD + OD))

            if D > max_D:
                max_D = D
                max_A_roll = i
                max_CR_roll = j
                max_CD_roll = k

    # Check duplicates for global maximum.
    maximum_count = 0
    for i in range(0, N+1):
        for j in range(0, N+1-i):
            k = N - i - j

            A = i * N_A
            CR = j * N_CR
            CD = k * N_CD
            D = (B * (1.0 + A + O) + F) * (1.0 + (CR + OR) * (CD + OD))

            if D == max_D:
                maximum_count += 1
    if maximum_count > 1:
        pass
        # print('Multiple optimal solutions.', sword_name)

    return max_A_roll, max_CR_roll, max_CD_roll


def apply_optimal_artifact_substat(kaeya, swords, artifact_main_stats, artifact_set_bonus):
    all_results = []
    partial_stats = dict()
    for sword_name in swords:                             # Loop over all swords.
        sword = swords[sword_name]
        for mainstat_name in artifact_main_stats:         # Loop over all artifact main stat combinations.
            mainstat = artifact_main_stats[mainstat_name]
            for artifact_set_name in artifact_set_bonus:  # Loop over all artifact set bonus.
                artifact_set = artifact_set_bonus[artifact_set_name]
                for refinement in range(5):               # Loop over all sword refinements.
                    current_row = [sword_name, str(refinement+1), artifact_set_name, mainstat_name]
                    for N in [18, 20, 25]:                # Loop over total desirable substat rolls.
                        # Character base attack.
                        B = kaeya.atk['80'] + sword['ATK@90']
                        # Non-artifact substat ATK%.
                        O = sword['ATK%@90'] + sword['ATK%@R1'] + refinement * sword['ATK%/R'] + mainstat['ATK%'] + artifact_set['ATK%']
                        # Non-artifact substat flat attack.
                        F = sword['ATK@R1'] + refinement * sword['ATK/R'] + mainstat['ATK']
                        # Non-artifact substat crit rate.
                        OR = sword['CR@R1'] + refinement * sword['CR/R'] + mainstat['CR'] + artifact_set['CR'] + 0.05
                        # Non-artifact substat crit dmg.
                        # Note: no swords give CD so far.
                        OD = mainstat['CD'] + 0.5

                        max_A_r, max_CR_r, max_CD_r = brute_force_substat_optimizer(B, O, F, OR, OD, N, sword_name)
                        substat_investment = '/'.join([str(max_A_r), str(max_CR_r), str(max_CD_r)])
                        current_row.append(substat_investment)

                        if N == 20:
                            key = '|'.join(current_row[0:4] + [substat_investment])
                            partial_stats[key] = [B, F,
                                                  O + max_A_r * N_A,
                                                  OR + max_CR_r * N_CR,
                                                  OD + max_CD_r * N_CD]
                    all_results.append(current_row)

    column_names = ['Sword', 'Refinement', 'Artifact set', 'Mainstats',
                    'Substat ATK%/CR/CD (N=18)', 'Substat ATK%/CR/CD (N=20)', 'Substat ATK%/CR/CD (N=25)']

    dir_path = os.path.dirname(os.path.realpath(__file__))
    result_file = os.path.join(dir_path, 'results/optimal_artifact_substat.tsv')
    with open(result_file, 'w') as file:
        file.write('\t'.join(column_names))
        file.write('\n')
        for result in all_results:
            file.write('\t'.join(result))
            file.write('\n')

    return partial_stats


def main():
    kaeya = Kaeya()
    swords = initialize_swords()
    artifact_set_bonus, artifact_main_stats = initialize_artifacts()
    partial_stats = apply_optimal_artifact_substat(kaeya, swords, artifact_main_stats, artifact_set_bonus)

    all_dmg_results = []
    column_names = ['Sword', 'Refinement', 'Artifact', 'Mainstat sand/gob/circ', 'Substat ATK%/CR/CD',
                    'AA1 DMG', 'CA DMG', 'AA1 infuse DMG', 'CA infuse DMG', 'E DMG', 'Q per hit DMG']

    # Generate the master spread sheet.
    for key in partial_stats:
        sword_name, refinement, artifact_set_name, mainstat_name, substat_investment = key.split('|')
        s = swords[sword_name]
        a = artifact_set_bonus[artifact_set_name]
        r = int(refinement) - 1
        B, F, A, CR, CD = partial_stats[key]

        # Normal attack dmg.
        aa_dmg = (B * (1 + A) + F) * (1 + CR * CD) * \
                 (1 + a['PDB'] + a['NADB'] + s['PDB@90'] + s['NADB@R1'] + r * s['NADB/R'] + s['ADB@R1'] + r * s['ADB/R']) * (1 + s['AS@R1'] + r * s['AS/R'])
        # Charged attack dmg.
        ca_dmg = (B * (1 + A) + F) * (1 + CR * CD) * \
                 (1 + a['PDB'] + a['CADB'] + s['PDB@90'] + s['CADB@R1'] + r * s['CADB/R'] + s['ADB@R1'] + r * s['ADB/R']) * (1 + s['AS@R1'] + r * s['AS/R'])
        # Normal attack dmg with cryo infusion.
        aa_infuse_dmg = (B * (1 + A) + F) * (1 + CR * CD) * \
                 (1 + a['CDB'] + a['NADB'] + s['NADB@R1'] + r * s['NADB/R'] + s['ADB@R1'] + r * s['ADB/R']) * (1 + s['AS@R1'] + r * s['AS/R'])
        # Charged attack dmg with cryo infusion.
        ca_infuse_dmg = (B * (1 + A) + F) * (1 + CR * CD) * \
                 (1 + a['CDB'] + a['CADB'] + s['CADB@R1'] + r * s['CADB/R'] + s['ADB@R1'] + r * s['ADB/R']) * (1 + s['AS@R1'] + r * s['AS/R'])
        # Elemental skill dmg.
        es_dmg = (B * (1 + A) + F) * (1 + (CR + s['ESCR@R1'] + r * s['ESCR/R']) * CD) * \
                 (1 + a['CDB'] + s['ESDB@R1'] + r * s['ESDB/R'] + s['ADB@R1'] + r * s['ADB/R'])
        # Elemental burst dmg.
        eb_dmg = (B * (1 + A) + F) * (1 + CR * CD) * \
                 (1 + a['CDB'] + a['EBDB'] + s['ADB@R1'] + r * s['ADB/R'])

        aa_dmg *= kaeya.skills['aa1']['8']
        ca_dmg *= kaeya.skills['cat']['8']
        aa_infuse_dmg *= kaeya.skills['aa1']['8']
        ca_infuse_dmg *= kaeya.skills['cat']['8']
        es_dmg *= kaeya.skills['es']['8']
        eb_dmg *= kaeya.skills['eb_perhit']['8']

        current_row = key.split('|') + [str(aa_dmg), str(ca_dmg), str(aa_infuse_dmg),
                                        str(ca_infuse_dmg), str(es_dmg), str(eb_dmg)]
        all_dmg_results.append(current_row)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    result_file = os.path.join(dir_path, 'results/master_weapon_artifact.tsv')
    with open(result_file, 'w') as file:
        file.write('\t'.join(column_names))
        file.write('\n')
        for result in all_dmg_results:
            file.write('\t'.join(result))
            file.write('\n')


if __name__ == "__main__":
    main()
