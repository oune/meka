<script>
    import Chart from "svelte-frappe-charts";
    import { io } from "socket.io-client";
    const socket = io("http://localhost:3000/");
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

    socket.on("connect", () => {
        console.log(`sensor connected on id: ${socket.id}`);
    });

    export let chartRefRumble;
    export let charRefTemperature;

    socket.on("data", (arg) => {
        console.log(arg);
        chartRefRumble.addDataPoint("Wed", [arg]);

        charRefTemperature.removeDataPoint(0);
        charRefTemperature.addDataPoint("wed", [arg]);
    });
</script>

<div>
    <h3>진동</h3>
    <Chart {data} type="line" bind:this={chartRefRumble} />
    <h3>온도</h3>
    <Chart {data} type="line" bind:this={charRefTemperature} />
</div>
