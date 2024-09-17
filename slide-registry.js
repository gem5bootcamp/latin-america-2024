window.get_slide_registry = function() {
    return [
        {
            "name": "01-Introduction",
            "slides": [
                "00-introduction-to-bootcamp",
                "01-simulation-background",
                "02-getting-started",
                "03-python-background"
            ]
        },
        {
            "name": "02-Using-gem5",
            "slides": [
                "01-stdlib",
                "02-gem5-resources",
                "03-running-in-gem5",
                "04-cores",
                "05-cache-hierarchies",
                "06-memory",
                "07-full-system",
                "08-accelerating-simulation",
                "09-sampling",
                "10-modeling-power",
                "11-multisim"
            ]
        },
        {
            "name": "03-Developing-gem5-models",
            "slides": [
                "01-sim-objects-intro",
                "02-debugging-gem5",
                "03-event-driven-sim",
                "04-ports",
                "05-modeling-cores",
                "06-modeling-cache-coherence",
                "07-chi-protocol",
                "08-ruby-network",
                "09-extending-gem5-models"
            ],
        },
        {
            "name": "04-GPU-model",
            "slides": [
                "01-GPU-model"
            ]
        },
        {
            "name": "05-Other-simulators",
            "slides": [
                "01-sst",
                "02-dram",
                "03-systemc"
            ]
        },
        {
            "name": "06-Contributing",
            "slides": [
                "01-contributing",
                "02-testing",
                "03-gem5-at-home"
            ]
        }
    ];
}
