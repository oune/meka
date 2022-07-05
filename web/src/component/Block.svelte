<script>
    import Sensor from "./Sensor.svelte";

    export let sensorNum;
    export let vibrationPort;
</script>

<div>
    <h2>
        {sensorNum}번 포트
    </h2>
    <Sensor port={vibrationPort} />
</div>
