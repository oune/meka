<script>
    import Chart from "svelte-frappe-charts";
    import { io } from "socket.io-client";
    export let sensorNum = 0;

    const socket = io("http://localhost:3000/");
    let data = {
        labels: ["start"],
        datasets: [
            {
                values: [0],
            },
        ],
    };

    socket.on("connect", () => {
        console.log(`sensor connected on id: ${socket.id}`);
    });

    let chartRefRumble;
    let charRefTemperature;

    socket.on("data", (arg) => {
        const { vibe, temp } = arg;

        chartRefRumble.addDataPoint("label", [vibe]);
        charRefTemperature.addDataPoint("label", [temp]);
    });
</script>

<div>
    <h2>
        {sensorNum}번 센서
    </h2>
    <h3>진동</h3>
    <Chart {data} type="line" bind:this={chartRefRumble} />
    <h3>온도</h3>
    <Chart {data} type="line" bind:this={charRefTemperature} />
</div>
