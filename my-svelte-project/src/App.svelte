<script>
    import Sensor from "./component/sensor.svelte";
    import Demo from "./component/test.svelte";
</script>

<h1>고장 진단 시스템</h1>
<div class="sensorContainer">
    <Sensor sensorNum="1" />
    <Sensor sensorNum="2" />
    <Sensor sensorNum="3" />
    <Sensor sensorNum="4" />

    <Demo />
</div>

<style>
    .sensorContainer {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
    }
</style>
