<script>
    import Sensor from "./Sensor.svelte";

    export let sensorNum;
    export let vibrationPort;
    export let temperaturePort;
</script>

<div>
    <h2>
        {sensorNum}번 센서
    </h2>
    <Sensor port={vibrationPort} />
    <!-- <h3>온도</h3>
    <Sensor port={temperaturePort} /> -->
</div>
