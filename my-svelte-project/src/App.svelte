<script>
    import Block from "./component/Block.svelte";
</script>

<h1>고장 진단 시스템</h1>
<div class="sensorContainer">
    <Block sensorNum="1" vibrationPort="3001" temperaturePort="3005" />
    <Block sensorNum="2" vibrationPort="3002" temperaturePort="3006" />
    <Block sensorNum="3" vibrationPort="3003" temperaturePort="3007" />
    <Block sensorNum="4" vibrationPort="3004" temperaturePort="3008" />
</div>

<style>
    .sensorContainer {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
    }
</style>
