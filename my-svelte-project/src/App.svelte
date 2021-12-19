<script>
    import Sensor from "./component/sensor.svelte";

    function addDataPoint() {
        chartRef.addDataPoint("Wed", [Math.random() * 20]);

        charRef1.removeDataPoint(0);
        charRef1.addDataPoint("wed", [Math.random() * 20]);
    }
</script>

<h1>고장 진단 시스템</h1>
<div class="sensorContainer">
    <Sensor sensorNum="1" />
    <Sensor sensorNum="2" />
    <Sensor sensorNum="3" />
    <Sensor sensorNum="4" />
</div>

<button on:click={addDataPoint}>Add data point</button>

<style>
    .sensorContainer {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
    }
</style>
