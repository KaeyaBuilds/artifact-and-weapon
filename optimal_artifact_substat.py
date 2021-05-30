# Here we optimize for the best investments for artifact substats.
# 1. We only consider weapon and artifact main stats.
# 2. We don't consider artifact set bonuses. Set bonuses shouldn't significantly change our end results.

import os
from data.kaeyastats import Kaeya
from data.swords import initialize_swords
from data.artifacts import initialize_artifacts


def brute_force_optimize(B, O, F, OR, OD, N, sword_name):
    # Reference:
    # The probability of all 25 substat rolls going into ATK% or CD or CR is: 0.75^25 = 0.0752%
    # The probability of at least 20 rolls going into ATK% or CD or CR is: 0.75^25+...+0.75^20 = 1.042%
    # The probability of at least 15 rolls going into ATK% or CD or CR is: 0.75^25+...+0.75^15 = 5.119%
    # The probability of at least 10 rolls going into ATK% or CD or CR is: 0.75^25+...+0.75^10 = 22.29%
    # The probability of at least 5 rolls going into ATK% or CD or CR is: 0.75^25+...+0.75^5 = 94.69%

    N_A = 0.04975
    N_CR = 0.033
    N_CD = 0.066

    max_D = -1
    max_A = 0
    max_CR = 0
    max_CD = N
    for i in range(0, N+1):
        for j in range(0, N+1-i):
            k = N - i - j

            A = i * N_A
            CR = j * N_CR
            CD = k * N_CD
            D = (B * (1.0 + A + O) + F) * (1.0 + (CR + OR) * (CD + OD))

            if D > max_D:
                max_A = i
                max_CR = j
                max_CD = k
                max_D = D

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
        print('Multiple optimal solutions.', sword_name)

    return max_A, max_CR, max_CD


def main():
    kaeya = Kaeya()
    swords = initialize_swords()
    artifact_set_bonus, artifact_main_stats = initialize_artifacts()

    all_results = []
    for sword_name in swords:
        sword = swords[sword_name]
        for mainstat_name in artifact_main_stats:
            mainstat = artifact_main_stats[mainstat_name]
            for artifact_set_name in artifact_set_bonus:
                artifact_set = artifact_set_bonus[artifact_set_name]
                for refinement in range(5):
                    current_row = [sword_name, str(refinement+1), artifact_set_name, mainstat_name]
                    for N in [15, 20, 25]:
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

                        max_A, max_CR, max_CD = brute_force_optimize(B, O, F, OR, OD, N, sword_name)
                        current_row.append('/'.join([str(max_A), str(max_CR), str(max_CD)]))

                    all_results.append(current_row)

    column_names = ['Sword', 'Refinement', 'Artifact set', 'Mainstats',
                    'Substat ATK%/CR/CD (N=15)', 'Substat ATK%/CR/CD (N=20)', 'Substat ATK%/CR/CD (N=25)']

    dir_path = os.path.dirname(os.path.realpath(__file__))
    result_file = os.path.join(dir_path, 'results/optimal_artifact_substat.tsv')
    with open(result_file, 'w') as file:
        file.write('\t'.join(column_names))
        file.write('\n')
        for result in all_results:
            file.write('\t'.join(result))
            file.write('\n')


if __name__ == "__main__":
    main()
