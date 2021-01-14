class PlannerConfig:

    run_plan = {
        "rank_programming_languages": True,
        "rank_public_clouds": True,
        "rank_degrees": True,
    }


class AnalyzerLanguagesConfig:

    programming_languages = [
        "python",
        "go",
        "golang",
        "java",
        "c",
        "c++",
        "javascript",
        "ruby",
        "php",
    ]

    public_clouds = [
        "aws",
        "azure",
        "gcp",
    ]


class AnalyzerDegreesConfig:
    bs_degrees = [
        "bachelor's degree",
        "bachelor degree",
    ]
    ms_degrees = [
        "master's degree",
        "master degree",
    ]
