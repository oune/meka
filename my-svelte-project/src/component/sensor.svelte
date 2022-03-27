<script>
    import Chart from "svelte-frappe-charts";
    import { io } from "socket.io-client";
    export let sensorNum = 0;

    const port = Number(sensorNum) + 3000;
    const url = `http://localhost:3010/`;
    const socket = io(url);

    let data = {
        labels: [],
        datasets: [{ values: [] }],
    };

    socket.on("connect", () => {
        console.log(`sensor connected on id: ${socket.id}`);
    });

    socket.emit("join", port.toString());

    let chartRefRumble;
    let charRefTemperature;

    let count = 0;
    socket.on("data", (arg) => {
        // const { vibe, temp } = arg;
        const { date, data } = arg;

        chartRefRumble.addDataPoint(date, [data]);
        // charRefTemperature.addDataPoint(".", [temp]);

        if (count > 50) {
            charRefTemperature.removeDataPoint(0);
            chartRefRumble.removeDataPoint(0);
        } else {
            count++;
        }
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
