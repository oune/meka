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

    let count = 0;
    let isEmpty = true;
    let port = 0;

    socket.emit("join", port.toString());

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
        const predicted = res.res.predicted.some((e) => {
            return e === 1;
        })
            ? 1
            : -1;
        model_res = predicted;
        isEmpty = false;

        if (model_res == -1) {
            detectError(port);
        }

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
        <Block sensorNum="1" />
        <Block sensorNum="2" />
        <Block sensorNum="3" />
        <Block sensorNum="4" />
    </div>
</body>

<style>
    .sensorContainer {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
    }
</style>
