<script>
    import Chart from "svelte-frappe-charts";
    import { io } from "socket.io-client";
    import { Jumper } from "svelte-loading-spinners";

    Notification.requestPermission();

    let model_res = true;
    let isReloading = true;

    const url = `http://localhost:8000`;
    const socket = io(url);

    socket.on("connect", () => {
        console.log(`sensor connected on id: ${socket.id}`);
        isReloading = false;
    });

    socket.on("connect_error", () => {
        isReloading = true;
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
    <div id="header">
        <h1>고장 진단 시스템</h1>
        <h2 id="reload">
            {#if isReloading}
                <Jumper size="60" color="#004fff" unit="px" duration="1s" />
                서버 접속중...
            {/if}
        </h2>
    </div>
    <h2>
        상태 : {#if isReloading}
            🌀 연결 끊김
        {:else if model_res}
            ✅ 정상
        {:else}
            ❌ 이상 감지됨
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
    #header {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }

    #reload {
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    h2 {
        margin: 0;
    }

    button {
        width: 120px;
        height: 40px;
        color: #fff;
        background: #004fff;
        font-size: 16px;
        border: none;
        border-radius: 20px;
        box-shadow: 0 4px 16px rgba(0, 79, 255, 0.3);
        transition: 0.3s;
        left: 50%;
        top: 50%;
    }
    button:focus {
        outline: 0;
    }
    button:hover {
        background: rgba(0, 79, 255, 0.9);
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(0, 79, 255, 0.6);
    }
</style>
