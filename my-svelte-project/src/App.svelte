<script>
    import Sensor from "./component/sensor.svelte";
</script>

<h1>고장 진단 시스템</h1>
<div class="sensorContainer">
    <Sensor sensorNum="0" />
    <Sensor sensorNum="1" />
    <Sensor sensorNum="2" />
    <Sensor sensorNum="3" />
</div>

<style>
    .sensorContainer {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
    }
</style>
