import * as d3 from "d3";
import { useRef, useEffect } from "react";

import { VisualTools } from "../../../tools/VisualTools";


// Reference: https://observablehq.com/@d3/horizontal-bar-chart/2
export function Histogram({data, freqAtt, binAtt, textAtt, compareFunc, 
    title="", yAxisTitle="", xAxisTitle="", figureProps}) {
    const ref = useRef();

    // Specify the chart’s dimensions, based on a bar’s height.
    const barHeight = 50;
    const marginTop = 180;
    const marginRight = 100;
    const marginBottom = 10;
    const marginLeft = 200;
    const graphWidth = 800;

    const width = marginLeft + graphWidth + marginRight;
    const height = Math.ceil((data.length + 0.1) * barHeight) + marginTop + marginBottom;

    const headingFontSize = 30;
    const axesFontSize = 24;
    const tickFontSize = 14;

    useEffect(() => {
        if (compareFunc) {
            data.sort(compareFunc);
        }

        const svgContainer = d3.select(ref.current);
        svgContainer.selectAll("*").remove();

        // Create the scales.
        const x = d3.scaleLinear()
            .domain([0, d3.max(data, d => d[freqAtt])])
            .range([marginLeft, width - marginRight]);

        const y = d3.scaleBand()
            .domain(d3.sort(data, d => -d[freqAtt]).map(d => d[binAtt]))
            .rangeRound([marginTop, height - marginBottom])
            .padding(0.1);

        // Create the SVG container.
        const svg = svgContainer
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr("style", "max-width: 100%; height: auto;");

        svg.selectAll("*").remove();

        // heading
        const heading = svg.append("g")
            .append("text")
            .attr("text-anchor", "middle")
            .attr("font-size", headingFontSize)
            .attr("x", marginLeft + graphWidth / 2)
            .attr("y", headingFontSize * 1.25)
            .style("font-weight", "bold");

        VisualTools.drawText({textGroup: heading, text: title, width: graphWidth, fontSize: headingFontSize, textX: marginLeft + graphWidth / 2});

        // Append a rect for each letter.
        svg.append("g")
            .attr("fill", "var(--mui-palette-primary-main)")
            .selectAll()
            .data(data)
            .join("rect")
                .attr("x", x(0))
                .attr("y", (d) => y(d[binAtt]))
                .attr("width", (d) => x(d[freqAtt]) - x(0))
                .attr("height", y.bandwidth());

        // Create the axes.
        const xAxis = svg.append("g");
        const xAxisLine = xAxis.append("g")
            .attr("transform", `translate(0,${marginTop})`)
            .call(d3.axisTop(x))
            .attr("font-size", tickFontSize);

        const xAxisLabel = xAxis.append("text")
            .transition()
            .attr("font-size", axesFontSize)
            .attr("x", marginLeft + graphWidth / 2)
            .attr("y", marginTop - axesFontSize * 2)
            .text(xAxisTitle);

        const yAxis = svg.append("g");
        const yAxisLine = yAxis.append("g")
            .attr("transform", `translate(${marginLeft},0)`)
            .call(d3.axisLeft(y).tickFormat((binLabel, binInd) => {
                return textAtt ? data[binInd][textAtt] : binLabel; 
            }))
            .attr("font-size", tickFontSize);

        const yAxisLabel = yAxis.append("text")
            .transition()
            .attr("font-size", axesFontSize)
            .attr("transform", "rotate(-90)")
            .attr("text-anchor", "middle")
            .attr("y", marginLeft / 4)
            .attr("x", -((height + marginTop) / 2))
            .text(yAxisTitle);
    }, [data]);

    return (
        <figure ref={ref} {...figureProps}></figure>
    );
}