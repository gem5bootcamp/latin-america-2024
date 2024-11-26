window.get_slide_registry = function() {
    return [
        {
            "name": "00-Pre-bootcamp",
            "slides": [
                "00-pre-bootcamp",
                "01-python-background",
            ],
        },
        {
            "name": "01-Introduction",
            "slides": [
                "00-introduction-to-bootcamp",
                "01-arch-research",
                "02-simulation-background",
                "03-getting-started",
            ]
        },
        {
            "name": "02-Using-gem5",
            "slides": [
                "01-stdlib",
                "02-memory",
                "03-traffic-generators",
                "04-cache-hierarchies",
                "05-cores",
                "06-custom-benchmarks",
                "07-gem5-resources",
                "08-multisim"
            ]
        },
        {
            "name": "03-Developing-gem5-models",
            "slides": [
                "01-sim-objects-intro",
                "02-debugging-gem5",
                "03-event-driven-sim",
                "04-ports"
            ],
        },
        {
            "name": "04-Advanced-using-gem5",
            "slides": [
                "01-full-system",
                "02-accelerating-simulation",
                "03-sampling",
                "04-gem5-at-home"
            ]
        }
    ];
}
