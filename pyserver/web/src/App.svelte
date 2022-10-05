<script>
    import Chart from "svelte-frappe-charts";
    import { io } from "socket.io-client";

    Notification.requestPermission();

    let model_res = true;

    const url = `http://localhost:8000`;
    const socket = io(url);

    socket.on("connect", () => {
        console.log(`sensor connected on id: ${socket.id}`);
    });

    socket.on("data", (arg) => {
        const { sensor_id, time } = arg;

        sensors[sensor_id].lastUpdate = time;
    });

    socket.on("model", (arg) => {
        const { time, mse, result } = arg;
        model_res = result;

        chartRef.addDataPoint(time, [mse]);

        if (result == false) {
            detectError();
        }
    });

    function detectError() {
        let notification;
        let notificationPermission = Notification.permission;
        if (notificationPermission === "granted") {
            notification = new Notification(`고장감지 시스템`, {
                body: `장치에서 고장이 감지됨`,
            });
        }
    }

    let chartRef;

    let data = {
        labels: [],
        datasets: [{ values: [] }],
        yMarkers: [
            {
                label: "Threshold",
                value: 0.000833,
                options: { labelPos: "left" }, // default: 'right'
            },
        ],
    };

    const lineOptions = {
        hideDots: 0,
        spline: 1,
        regionFill: 1,
    };

    const sensors = [
        { name: "센서1", lastUpdate: "empty" },
        { name: "센서2", lastUpdate: "empty" },
        { name: "센서3", lastUpdate: "empty" },
        { name: "센서4", lastUpdate: "empty" },
    ];

    const onExport = () => chartRef.exportChart();
</script>

<body>
    <h1>고장 진단 시스템</h1>
    <h2>
        상태 : {#if model_res == true}
            ✅ 정상
        {:else}
            ❗이상 감지됨
        {/if}
    </h2>
    <Chart
        {data}
        type="line"
        {lineOptions}
        animate="false"
        bind:this={chartRef}
    />
    <button on:click={onExport}> save </button>
    {#each sensors as { name, lastUpdate }, i}
        <h2>
            {name} : {lastUpdate}
        </h2>
    {/each}
</body>

<style>
</style>
