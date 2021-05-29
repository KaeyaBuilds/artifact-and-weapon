# Here we optimize for the best investments for artifact substats.
# 1. We only consider weapon and artifact main stats.
# 2. We don't consider artifact set effects. Set effects shouldn't drastically change the end results.

from data.swords import initialize_swords


def main():
    swords = initialize_swords()

    for sword in swords:
        print(swords[sword])
        # We follow the formula at the end of this document:
        # https://github.com/KaeyaBuilds/artifact-and-weapon/blob/main/doc/optimal_artifact_substat_formula.pdf
        B = 0
        O = 0
        F = 0
        OR = 0
        OD = 0


if __name__ == "__main__":
    main()
