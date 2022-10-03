<script>
    export let sensorNum;
    let chartRef;

    import Chart from "svelte-frappe-charts";

    export let data = {
        labels: [],
        datasets: [{ values: [] }],
    };
    const axisOptions = {
        xIsSeries: true, // default: false
    };

    const lineOptions = {
        hideDots: 1,
        spline: 1,
    };

    const onExport = () => chartRef.exportChart();
</script>

<div>
    <h2>
        {sensorNum}번 포트
    </h2>

    {#if data.labels.length}
        <Chart
            {data}
            type="line"
            {axisOptions}
            {lineOptions}
            bind:this={chartRef}
        />
    {:else}
        <p>수신한 데이터가 없습니다.</p>
    {/if}
    <button on:click={onExport}> save </button>
</div>
