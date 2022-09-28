<script>
    import Block from "./component/SensorBlock.svelte";

    Notification.requestPermission();
</script>

<body>
    <h1>고장 진단 시스템</h1>
    <div class="sensorContainer">
        <Block sensorNum="1" port="3001" />
        <Block sensorNum="2" port="3002" />
        <Block sensorNum="3" port="3003" />
        <Block sensorNum="4" port="3004" />
    </div>
</body>

<style>
    .sensorContainer {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
    }
</style>
