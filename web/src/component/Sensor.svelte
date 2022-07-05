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
    let model_res = 0;

    socket.on("data", (arg) => {
        const { date, data } = arg;
        isEmpty = false;

        chartRef.addDataPoint(date, [data]);

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

    socket.on("model_result", (res) => {
        const predicted = res.res.predicted[0];
        model_res = predicted;
        isEmpty = false;

        const scores = res.res.score;
        const predicts = res.res.predicted;

        data = {
            labels: predicts,
            datasets: [
                {
                    values: scores,
                },
            ],
        };
        console.log(scores);
        console.log(data);
    });

    let selected = "none";
    let options = [
        { id: "none", text: `센서 없음` },
        { id: "pump", text: `펌프 진동센서` },
        { id: "motor", text: `모터 진동센서` },
    ];

    function select_change() {
        socket.emit("mode", {
            port: port.toString(),
            mode: selected.id,
        });
        model_res = 0;
        isEmpty = true;
    }
</script>

<h2>
    상태 : {#if model_res == 1}
        ✅ 정상
    {:else if model_res == -1}
        ❗이상 감지됨
    {:else}
        대기중
    {/if}
</h2>

<form>
    <select bind:value={selected} on:change={select_change}>
        {#each options as option}
            <option value={option.id}>
                {option.text}
            </option>
        {/each}
    </select>
</form>

{#if isEmpty}
    <p>수신한 모델 결과가 없습니다.</p>
{:else}
    <Chart {data} type="line" bind:this={chartRef} />
{/if}
