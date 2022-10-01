<script>
    import Block from "./component/SensorBlock.svelte";
    import { io } from "socket.io-client";

    Notification.requestPermission();

    let model_res = 1;

    const url = `http://localhost:3000`;
    const socket = io(url);

    socket.on("connect", () => {
        console.log(`sensor connected on id: ${socket.id}`);
    });

    const datas = [
        {
            labels: ["1", "2", "3"],
            datasets: [{ values: [1, 2, 3] }],
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
        const { sensor_id, time, data } = arg;

        // id 에 따른 데이터 업데이트
    });

    function detectError(port) {
        let notification;
        let notificationPermission = Notification.permission;
        if (notificationPermission === "granted") {
            //Notification을 이미 허용한 사람들에게 보여주는 알람창
            notification = new Notification(`고장감지 시스템`, {
                body: `${port - 3000}포트 ${selected} 고장이 감지됨`,
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
