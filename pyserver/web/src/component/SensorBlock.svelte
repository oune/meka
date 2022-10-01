<script>
    export let sensorNum;
    export let chartRef;

    import Chart from "svelte-frappe-charts";

    export let data = {
        labels: [],
        datasets: [{ values: [] }],
    };
</script>

<div>
    <h2>
        {sensorNum}번 포트
    </h2>

    {#if data.labels.length}
        <Chart {data} type="line" bind:this={chartRef} />
    {:else}
        <p>수신한 데이터가 없습니다.</p>
    {/if}
</div>
