<script>
    import Block from "./component/Block.svelte";
</script>

<body>
    <h1>고장 진단 시스템</h1>
    <div class="sensorContainer">
        <Block sensorNum="1" vibrationPort="1" />
        <Block sensorNum="2" vibrationPort="2" />
        <Block sensorNum="3" vibrationPort="3" />
        <Block sensorNum="4" vibrationPort="4" />
    </div>
</body>

<style>
    .sensorContainer {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
    }
</style>
