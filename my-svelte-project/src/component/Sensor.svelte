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
    let isEmpty = true;

    socket.on("data", (arg) => {
        const { date, data } = arg;
        isEmpty = false;

        chartRef.addDataPoint(date, [data]);
        console.log(count);

        if (count > 50) {
            chartRef.removeDataPoint(0);
        } else {
            count++;
        }
    });

    let data = {
        labels: [],
        datasets: [{ values: [] }],
    };

    let selected;
    let options = [
        { id: 1, text: `온도센서` },
        { id: 2, text: `모터 진동센서` },
        { id: 3, text: `펌프 진동센서` },
    ];
</script>

<form>
    <select bind:value={selected}>
        {#each options as option}
            <option value={option}>
                {option.text}
            </option>
        {/each}
    </select>
</form>

{#if isEmpty}
    <p>수신한 데이터가 없습니다.</p>
{:else}
    <Chart {data} type="line" bind:this={chartRef} />
{/if}
