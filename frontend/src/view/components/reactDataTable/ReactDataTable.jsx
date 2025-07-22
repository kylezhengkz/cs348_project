import "./styles.css"

import $ from 'jquery';
import DataTable from 'datatables.net-bs5';
import { useRef, useEffect } from 'react';


export function ReactDataTable({data, columns, tableContainerProps, tableProps, dataTableKwargs}) {
    const ref = useRef();

    if (tableContainerProps === undefined) {
        tableContainerProps = {};
    }

    let containerClsName = "tableContainer";
    if (tableContainerProps["className"] !== undefined) {
        containerClsName += " " + tableContainerProps["className"];
    } 

    require('../../../resources/booking_icon.jpg')

    useEffect(() => {
        const dataTable = $(ref.current).DataTable({
            data: data,
            columns: columns,
            destroy: true,
            scrollCollapse: true,
            scrollX: true,
            scrollY: '300px',
            ...dataTableKwargs
        });

        return () => {
            dataTable.destroy();
        }
    }, [data, columns]);

    return (
        <div className={containerClsName} {...tableContainerProps}>
            <table ref={ref} {...tableProps}></table>
        </div>
    );
}