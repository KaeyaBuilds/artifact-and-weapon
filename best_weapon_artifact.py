# (c)2021 wolich at Kaeya Mains

from data.kaeyastats import Kaeya
from data.swords import initialize_swords
from data.artifacts import initialize_artifacts
from utils.io import write_result_file

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

            if D > max_D and CR + OR <= 1.0:
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
                        OR = sword['CR@90'] + sword['CR@R1'] + refinement * sword['CR/R'] + mainstat['CR'] + artifact_set['CR'] + 0.05
                        # Non-artifact substat crit dmg.
                        # Note: no swords give CD so far.
                        OD = sword['CD@90'] + mainstat['CD'] + 0.5

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

    write_result_file('../results/optimal_artifact_substat.tsv', column_names, all_results)

    return partial_stats


def calculate_best_build_for_weapon(all_dmg_results, dmg_col):
    best_build = dict()
    # If phys build.
    if dmg_col == 6 or dmg_col == 8 or dmg_col == 9:
        forbidden_artifacts = ['4-pf 1 stack', '4-pf 2 stacks', '4-bc with active', '4-bs cryo', '4-bs frozen', '4-no with active']
    # If cryo build.
    else:
        forbidden_artifacts = ['4-pf 1 stack', '4-pf 2 stacks', '4-bc with active', '4-no with active']

    allowed_stars = ['5', '4', '3']
    for result in all_dmg_results:
        key = result[0] + result[1]
        # If the sword is R1 or R5 4/3* and valid artifact set and either there is no record of the sword yet,
        # or a new build is better than the current best build.
        if result[5] in allowed_stars and (result[1] == '1' or (result[1] == '5' and result[5] != '5')) and \
           result[2] not in forbidden_artifacts and \
           (key not in best_build or float(best_build[key][-1]) < float(result[dmg_col])):
            best_build[key] = result[1:5] + [result[dmg_col]]

    # [key][:-1] is to recover the sword name and get rid of the refinement.
    best_build = [[key[:-1]] + best_build[key] for key in best_build]
    best_build.sort(reverse=True, key=lambda x: float(x[-1]))

    return best_build


def main():
    kaeya = Kaeya()
    swords = initialize_swords()
    artifact_set_bonus, artifact_main_stats = initialize_artifacts()
    partial_stats = apply_optimal_artifact_substat(kaeya, swords, artifact_main_stats, artifact_set_bonus)

    all_dmg_results = []
    column_names = ['Sword', 'Refinement', 'Artifact', 'Mainstat sand/gob/circ', 'Substat ATK%/CR/CD', 'Star',
                    'Phys Kaeya rotation DMG', 'Cryo Kaeya rotation DMG', 'AA1 DMG', 'CA DMG', 'AA1 infuse DMG', 'CA infuse DMG', 'E DMG', 'Q per hit DMG']

    ########################################
    # Generate the master spread sheet.
    ########################################
    for key in partial_stats:
        sword_name, refinement, artifact_set_name, mainstat_name, substat_investment = key.split('|')
        s = swords[sword_name]
        a = artifact_set_bonus[artifact_set_name]
        m = artifact_main_stats[mainstat_name]
        r = int(refinement) - 1
        B, F, A, CR, CD = partial_stats[key]

        # Normal attack dmg.
        aa_dmg = (B * (1 + A) + F) * (1 + min(CR, 1.0) * CD) * \
                 (1 + m['PDB'] + a['PDB'] + a['NADB'] + s['PDB@90'] + s['NADB@R1'] + r * s['NADB/R'] + s['ADB@R1'] + r * s['ADB/R']) * (1 + s['AS@R1'] + r * s['AS/R'])
        # Charged attack dmg.
        ca_dmg = (B * (1 + A) + F) * (1 + min(CR, 1.0) * CD) * \
                 (1 + m['PDB'] + a['PDB'] + a['CADB'] + s['PDB@90'] + s['CADB@R1'] + r * s['CADB/R'] + s['ADB@R1'] + r * s['ADB/R']) * (1 + s['AS@R1'] + r * s['AS/R'])
        # Normal attack dmg with cryo infusion.
        aa_infuse_dmg = (B * (1 + A) + F) * (1 + min(CR, 1.0) * CD) * \
                 (1 + m['CDB'] + a['CDB'] + a['NADB'] + s['NADB@R1'] + r * s['NADB/R'] + s['ADB@R1'] + r * s['ADB/R']) * (1 + s['AS@R1'] + r * s['AS/R'])
        # Charged attack dmg with cryo infusion.
        ca_infuse_dmg = (B * (1 + A) + F) * (1 + min(CR, 1.0) * CD) * \
                 (1 + m['CDB'] + a['CDB'] + a['CADB'] + s['CADB@R1'] + r * s['CADB/R'] + s['ADB@R1'] + r * s['ADB/R']) * (1 + s['AS@R1'] + r * s['AS/R'])
        # Elemental skill dmg.
        es_dmg = (B * (1 + A) + F) * (1 + min((CR + s['ESCR@R1'] + r * s['ESCR/R']), 1.0) * CD) * \
                 (1 + m['CDB'] + a['CDB'] + s['ESDB@R1'] + r * s['ESDB/R'] + s['ADB@R1'] + r * s['ADB/R'])
        # Elemental burst dmg.
        eb_dmg = (B * (1 + A) + F) * (1 + min(CR, 1.0) * CD) * \
                 (1 + m['CDB'] + a['CDB'] + a['EBDB'] + s['ADB@R1'] + r * s['ADB/R'])

        # E > Q > N2C x 2 > E > N2C x 2. 10 hits on Q.
        basic_combo_phys = 4 * aa_dmg * (kaeya.skills['aa1']['8'] + kaeya.skills['aa2']['8']) + \
                           4 * ca_dmg * (kaeya.skills['cat']['8']) + \
                           2 * es_dmg * kaeya.skills['es']['8'] + \
                           10 * eb_dmg * kaeya.skills['eb_perhit']['8']
        basic_combo_cryo = 4 * aa_infuse_dmg * (kaeya.skills['aa1']['8'] + kaeya.skills['aa2']['8']) + \
                           4 * ca_infuse_dmg * (kaeya.skills['cat']['8']) + \
                           2 * es_dmg * kaeya.skills['es']['8'] + \
                           10 * eb_dmg * kaeya.skills['eb_perhit']['8']

        # Single abilities.
        aa_dmg *= kaeya.skills['aa1']['8']
        ca_dmg *= kaeya.skills['cat']['8']
        aa_infuse_dmg *= kaeya.skills['aa1']['8']
        ca_infuse_dmg *= kaeya.skills['cat']['8']
        es_dmg *= kaeya.skills['es']['8']
        eb_dmg *= kaeya.skills['eb_perhit']['8']

        current_row = key.split('|') + [str(int(s['Star']))] + \
                      [str(int(basic_combo_phys)), str(int(basic_combo_cryo)),
                       str(int(aa_dmg)), str(int(ca_dmg)), str(int(aa_infuse_dmg)),
                       str(int(ca_infuse_dmg)), str(int(es_dmg)), str(int(eb_dmg))]
        all_dmg_results.append(current_row)

    write_result_file('../results/master_weapon_artifact_sheet.tsv', column_names, all_dmg_results)

    ########################################
    # Generate viable builds.
    ########################################
    best_for_weapon_combop = calculate_best_build_for_weapon(all_dmg_results, 6)
    best_for_weapon_comboc = calculate_best_build_for_weapon(all_dmg_results, 7)
    best_for_weapon_aa = calculate_best_build_for_weapon(all_dmg_results, 8)
    best_for_weapon_ca = calculate_best_build_for_weapon(all_dmg_results, 9)
    best_for_weapon_aa_infuse = calculate_best_build_for_weapon(all_dmg_results, 10)
    best_for_weapon_ca_infuse = calculate_best_build_for_weapon(all_dmg_results, 11)
    best_for_weapon_e = calculate_best_build_for_weapon(all_dmg_results, 12)
    best_for_weapon_q = calculate_best_build_for_weapon(all_dmg_results, 13)

    column_names = ['Sword', 'Refinement', 'Artifact', 'Mainstat sand/gob/circ', 'Substat ATK%/CR/CD', 'Average DMG']
    write_result_file('../results/best_builds_for_phys_rotation.tsv', column_names, best_for_weapon_combop)
    write_result_file('../results/best_builds_for_cryo_rotation.tsv', column_names, best_for_weapon_comboc)
    write_result_file('../results/best_builds_for_AA1.tsv', column_names, best_for_weapon_aa)
    write_result_file('../results/best_builds_for_CA.tsv', column_names, best_for_weapon_ca)
    write_result_file('../results/best_builds_for_AA1infuse.tsv', column_names, best_for_weapon_aa_infuse)
    write_result_file('../results/best_builds_for_CAinfuse.tsv', column_names, best_for_weapon_ca_infuse)
    write_result_file('../results/best_builds_for_E.tsv', column_names, best_for_weapon_e)
    write_result_file('../results/best_builds_for_Q.tsv', column_names, best_for_weapon_q)


if __name__ == "__main__":
    main()
