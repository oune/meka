<script>
    import Block from "./component/SensorBlock.svelte";
    import { io } from "socket.io-client";

    Notification.requestPermission();

    let model_res = 1;

    const url = `http://localhost:8000`;
    const socket = io(url);

    socket.on("connect", () => {
        console.log(`sensor connected on id: ${socket.id}`);
    });

    const datas = [
        {
            labels: [],
            datasets: [{ values: [] }],
        },
        {
            labels: [],
            datasets: [{ values: [] }],
        },
        {
            labels: [],
            datasets: [{ values: [] }],
        },
        {
            labels: [],
            datasets: [{ values: [] }],
        },
    ];

    socket.on("data", (arg) => {
        const { sensor_id, data } = arg;

        const outData = data.slice(0, 25);

        // update chart
        datas[sensor_id] = {
            labels: [...Array(outData.length).keys()],
            datasets: [{ values: outData }],
        };
    });

    socket.on("model", (arg) => {
        //TODO 모델 결과를 받아서 화면을 변경
        const { result } = arg;
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
</script>

<body>
    <h1>고장 진단 시스템</h1>
    <h2>
        상태 : {#if model_res == 1}
            ✅ 정상
        {:else if model_res == -1}
            ❗이상 감지됨
        {:else}
            대기중
        {/if}
    </h2>
    <div class="sensorContainer">
        {#each datas as data, i}
            <Block sensorNum={i + 1} {data} />
        {/each}
    </div>
</body>

<style>
    .sensorContainer {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
    }
</style>
