<script>
    import Chart from "svelte-frappe-charts";
    export let sensorNum = 0;

    let data = {
        labels: [
            "Sun",
            "Mon",
            "Tues",
            "Wed",
            "Thurs",
            "Fri",
            "Sat",
            "Sun",
            "Mon",
            "Tues",
            "Wed",
            "Thurs",
            "Fri",
            "Sat",
        ],
        datasets: [
            {
                values: [10, 12, 3, 9, 8, 15, 9, 10, 12, 3, 9, 8, 15, 9],
            },
        ],
    };

    export let chartRefRumble;
    export let charRefTemperature;

    function addDataPoint() {
        chartRefRumble.addDataPoint("Wed", [Math.random() * 20]);

        charRefTemperature.removeDataPoint(0);
        charRefTemperature.addDataPoint("wed", [Math.random() * 20]);
    }
</script>

<div>
    <h2>
        {sensorNum}번 센서
    </h2>
    <h3>진동</h3>
    <Chart {data} type="line" bind:this={chartRefRumble} />
    <h3>온도</h3>
    <Chart {data} type="line" bind:this={charRefTemperature} />

    <button on:click={addDataPoint}>Add data point</button>
</div>
