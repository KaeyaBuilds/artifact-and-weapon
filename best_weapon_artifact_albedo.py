# (c)2021 wolich at Kaeya Mains

from data.character_stats import Albedo
from data.swords import initialize_swords
from data.artifacts import initialize_artifacts
from utils.io import write_result_file

# For 5 star artifacts.
# Average ATK% per ATK% substat roll.
N_A_5 = 0.04975
# Average DEF% per DEF% substat roll.
N_D_5 = 0.062
# Average CR per CR substat roll.
N_CR_5 = 0.033
# Average CD per CD substat roll.
N_CD_5 = 0.066

# For 4 star artifacts.
# Average ATK% per ATK% substat roll.
N_A_4 = 0.03975
# Average DEF% per DEF% substat roll.
N_D_4 = 0.04975
# Average CR per CR substat roll.
N_CR_4 = 0.0265
# Average CD per CD substat roll.
N_CD_4 = 0.053


def brute_force_substat_optimizer_on_drugs(albedo, sword, refinement, mainstat, artifact_set_name, artifact_set, N):
    # Reference:
    # The probability of all 25 substat rolls going into ATK% or CD or CR is: 0.75^25 = 0.0752%
    # The probability of at least 20 rolls going into ATK% or CD or CR is: 0.75^25+...+0.75^20 = 1.042%
    # The probability of at least 15 rolls going into ATK% or CD or CR is: 0.75^25+...+0.75^15 = 5.119%
    # The probability of at least 10 rolls going into ATK% or CD or CR is: 0.75^25+...+0.75^10 = 22.29%
    # The probability of at least 5 rolls going into ATK% or CD or CR is: 0.75^25+...+0.75^5 = 94.69%

    # Character base attack.
    B = albedo.atk['90'] + sword['ATK@90']
    # Non-artifact substat ATK%.
    O = sword['ATK%@90'] + sword['ATK%@R1'] + refinement * sword['ATK%/R'] + mainstat['ATK%'] + artifact_set['ATK%']
    # Non-artifact substat flat attack.
    F = sword['ATK@R1'] + refinement * sword['ATK/R'] + mainstat['ATK']
    # Character base defense. Note: No swords give flat DEF so far.
    BDEF = albedo.defense['90']
    # Non-artifact substat DEF%.
    ODEF = sword['DEF%@90'] + sword['DEF%@R1'] + refinement * sword['DEF%/R'] + mainstat['DEF%'] + artifact_set['DEF%']
    # Non-artifact substat crit rate.
    OR = sword['CR@90'] + sword['CR@R1'] + refinement * sword['CR/R'] + mainstat['CR'] + artifact_set['CR'] + 0.05
    # Non-artifact substat crit dmg. Note: no swords give CD so far.
    OD = sword['CD@90'] + mainstat['CD'] + 0.5

    # Discount for 4 star flower and feather when using Defender's or Gambler.
    # Note that for Jade Cutter, the code is using Kaeya's HP stats, which is ~10% lower than Albedo's.
    # Also, I don't correct for the 4 star flower for Jade Cutter.
    adjust = False
    if artifact_set_name.find('2-gamb') >= 0 or artifact_set_name.find('2-def') >= 0:
        B -= (311 - 232)
        adjust = True

    max_D_forRotation = -1
    max_A_roll_forRotation = N
    max_D_roll_forRotation = 0
    max_CR_roll_forRotation = 0
    max_CD_roll_forRotation = 0
    max_D_forE = -1
    max_A_roll_forE = N
    max_D_roll_forE = 0
    max_CR_roll_forE = 0
    max_CD_roll_forE = 0
    for i in range(0, N+1):
        for j in range(0, N+1-i):
            for k in range(0, N+1-i-j):
                l = max(0, N - i - j - k)
                assert i + j + k + l == N

                # Discount for 4-star flower and feather.
                # 3/5 artifacts are 5-star, 2/5 artifacts are 4-star.
                if adjust:
                    A = i * N_A_5 * 0.6 + i * N_A_4 * 0.4
                    DEF = j * N_D_5 * 0.6 + j * N_D_4 * 0.4
                    CR = k * N_CR_5 * 0.6 + k * N_CR_4 * 0.4
                    CD = l * N_CD_5 * 0.6 + l * N_CD_4 * 0.4
                else:
                    A = i * N_A_5
                    DEF = j * N_D_5
                    CR = k * N_CR_5
                    CD = l * N_CD_5

                s = sword
                a = artifact_set
                m = mainstat
                r = refinement

                dmg_aa1 = (B * (1 + A + O) + F) * (1 + min(1, (CR + OR)) * (CD + OD)) * \
                          (1 + a['PDB'] + s['PDB@90'] + s['NADB@R1'] + r * s['NADB/R'] + s[
                              'ADB@R1'] + r * s['ADB/R']) * (1 + s['AS@R1'] + r * s['AS/R']) * \
                          albedo.skills['aa1']['10']
                dmg_e_init = (B * (1 + A + O) + F) * (1 + min((CR + s['ESCR@R1'] + r * s['ESCR/R'] + OR), 1.0) * (CD + OD)) * \
                             (1 + albedo.gdb['80'] + m['GDB'] + a['GDB'] + a['ESDB'] + s['ESDB@R1'] + r * s['ESDB/R'] + s['ADB@R1'] + r * s['ADB/R']) * \
                             albedo.skills['es_init']['10']
                dmg_e_perhit = BDEF * (1 + DEF + ODEF) * (1 + min((CR + s['ESCR@R1'] + r * s['ESCR/R'] + OR), 1.0) * (CD + OD)) * \
                             (1 + albedo.gdb['80'] + m['GDB'] + a['GDB'] + a['ESDB'] + s['ESDB@R1'] + r * s['ESDB/R'] + s['ADB@R1'] + r * s['ADB/R']) * \
                             albedo.skills['es_perhit']['10']
                dmg_q_init = (B * (1 + A + O) + F) * (1 + min(1, (CR + OR)) * (CD + OD)) * \
                             (1 + albedo.gdb['80'] + m['GDB'] + a['GDB'] + a['EBDB'] + s['ADB@R1'] + r * s['ADB/R']) * \
                             albedo.skills['eb_init_c0']['10']
                dmg_q_perhit = (B * (1 + A + O) + F) * (1 + min(1, (CR + OR)) * (CD + OD)) * \
                               (1 + albedo.gdb['80'] + m['GDB'] + a['GDB'] + a['EBDB'] + s['ADB@R1'] + r * s['ADB/R']) * \
                               albedo.skills['eb_perhit_c0']['10']

                # 40 second rotation, resets E twice, 15 proc (not 20, room for error), one Q and 4 Q blossom hits.
                dmg_rotation = dmg_aa1 * 2 + dmg_e_init * 2 + dmg_e_perhit * 15 + dmg_q_init + dmg_q_perhit * 4

                if dmg_e_perhit > max_D_forE and CR + OR <= 1.0:
                    max_D_forE = dmg_e_perhit
                    max_A_roll_forE = i
                    max_D_roll_forE = j
                    max_CR_roll_forE = k
                    max_CD_roll_forE = l
                if dmg_rotation > max_D_forRotation and CR + OR <= 1.0:
                    max_D_forRotation= dmg_rotation
                    max_A_roll_forRotation = i
                    max_D_roll_forRotation = j
                    max_CR_roll_forRotation  = k
                    max_CD_roll_forRotation = l

    return max_D_forE, \
           max_A_roll_forE, \
           max_D_roll_forE, \
           max_CR_roll_forE, \
           max_CD_roll_forE, \
           max_D_forRotation, \
           max_A_roll_forRotation, \
           max_D_roll_forRotation, \
           max_CR_roll_forRotation, \
           max_CD_roll_forRotation


def generate_master_sheet(albedo, swords, artifact_main_stats, artifact_set_bonus):
    all_results = []
    for sword_name in swords:                             # Loop over all swords.
        sword = swords[sword_name]
        for mainstat_name in artifact_main_stats:         # Loop over all artifact main stat combinations.
            mainstat = artifact_main_stats[mainstat_name]
            for artifact_set_name in artifact_set_bonus:  # Loop over all artifact set bonus.
                artifact_set = artifact_set_bonus[artifact_set_name]
                for refinement in range(5):               # Loop over all sword refinements.
                    current_row = [sword_name, str(refinement+1), artifact_set_name, mainstat_name]
                    for N in [20]:                        # Loop over total desirable substat rolls.
                        r = brute_force_substat_optimizer_on_drugs(
                            albedo, sword, refinement, mainstat, artifact_set_name, artifact_set, N)

                        substat_investment_E = '/'.join([str(r[1]), str(r[2]), str(r[3]), str(r[4])])
                        substat_investment_rotation = '/'.join([str(r[6]), str(r[7]), str(r[8]), str(r[9])])
                        current_row.append(substat_investment_E)
                        current_row.append(substat_investment_rotation)
                        current_row.append(str(r[0]))
                        current_row.append(str(r[5]))

                        # This is here because we only do N = one value for now.
                        all_results.append(current_row)

    column_names = ['Sword', 'Refinement', 'Artifact set', 'Mainstats',
                    'E optimized substat ATK%/DEF%/CR/CD', 'Rotation optimized substat ATK%/DEF%/CR/CD',
                    'E optimized damage', 'Rotation optimized damage']

    write_result_file('../results/albedo/all_combinations.tsv', column_names, all_results)


def main():
    albedo = Albedo()
    swords = initialize_swords()
    artifact_set_bonus, artifact_main_stats = initialize_artifacts(unit='albedo')
    generate_master_sheet(albedo, swords, artifact_main_stats, artifact_set_bonus)


if __name__ == "__main__":
    main()
