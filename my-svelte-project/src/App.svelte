<script>
    import Block from "./component/block.svelte";
</script>

<h1>고장 진단 시스템</h1>
<div class="sensorContainer">
    <Block sensorNum="1" />
    <Block sensorNum="2" />
    <Block sensorNum="3" />
    <Block sensorNum="4" />
</div>

<style>
    .sensorContainer {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
    }
</style>
