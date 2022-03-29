<script>
    import Chart from "svelte-frappe-charts";
    import { io } from "socket.io-client";

    export let port;

    const url = `http://localhost:3000`;
    const socket = io(url);

    socket.on("connect", () => {
        console.log(`sensor connected on id: ${socket.id}`);
    });

    socket.emit("join", port.toString());

    let chartRef;
    let count = 0;

    socket.on("data", (arg) => {
        const { date, data } = arg;

        chartRef.addDataPoint(date, [data]);

        if (count > 50) {
            charRef.removeDataPoint(0);
        } else {
            count++;
        }
    });

    let data = {
        labels: [],
        datasets: [{ values: [] }],
    };
</script>

<div>
    <Chart {data} type="line" bind:this={chartRef} />
</div>
