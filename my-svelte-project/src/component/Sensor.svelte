<script>
    import Chart from "svelte-frappe-charts";
    import { io } from "socket.io-client";

    export let port;
    const url = `http://localhost:${port}/`;
    const socket = io(url);

    let data = {
        labels: [],
        datasets: [{ values: [] }],
    };

    socket.on("connect", () => {
        console.log(`sensor connected on id: ${socket.id}`);
    });

    socket.emit("join", port.toString());

    let charRef;

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
</script>

<div>
    <Chart {data} type="line" bind:this={charRef} />
</div>
