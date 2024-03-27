function get_order_total_price() {

    let nodeList = document.querySelectorAll(".order-line-price");
    let total_price = 0;
    for (let i = 0; i < nodeList.length; i++) {
        let order_line_price = nodeList[i].valueAsNumber
        if (Number.isInteger(order_line_price)) {total_price += Number(order_line_price);}
    }
    document.getElementById('order-total-price').innerHTML = total_price;
}

function addRow() {
    let table = document.getElementById("order-lines");

    let first_row = table.rows[0];
    let new_row = first_row.cloneNode(true);

    let number_table_rows = table.rows.length
    let stringToSplit = document.getElementById("orderTable").rows.item(number_table_rows).querySelector('[id]').id
    let new_row_id = Number(stringToSplit.split('-')[1]) + 1;

    new_row.cells[0].children[0].id = 'order_line-' + new_row_id + '-service_id';
    new_row.cells[0].children[0].name = 'order_line-' + new_row_id + '-service_id';
    new_row.cells[0].children[0].className = 'service_id';
    new_row.cells[0].children[0].value = '0';

    new_row.cells[1].children[0].id = 'order_line-' + new_row_id + '-quantity';
    new_row.cells[1].children[0].name = 'order_line-' + new_row_id + '-quantity';
    new_row.cells[1].children[0].value = 1;
    new_row.cells[1].children[0].removeAttribute('readonly');

    new_row.cells[2].children[0].id = 'order_line-' + new_row_id + '-unit';
    new_row.cells[2].children[0].name = 'order_line-' + new_row_id + '-unit';
    new_row.cells[2].children[0].value = '';

    new_row.cells[3].children[0].id = 'order_line-' + new_row_id + '-price';
    new_row.cells[3].children[0].name = 'order_line-' + new_row_id + '-price';
    new_row.cells[3].children[0].value = '';

    new_row.cells[4].children[0].id = 'order_line-' + new_row_id + '-order_line_price';
    new_row.cells[4].children[0].name = 'order_line-' + new_row_id + '-order_line_price';
    new_row.cells[4].children[0].value = '';

    new_row.cells[5].children[0].id = 'order_line-' + new_row_id + '-event_date';
    new_row.cells[5].children[0].name = 'order_line-' + new_row_id + '-event_date';
    new_row.cells[5].children[0].value= new Date().toJSON().slice(0, 10);

    new_row.cells[6].children[0].id = 'remove-order-line-enabled';

    table.appendChild(new_row);
}


function recountOrderLinePriceWhenChangingService(service_id_cell, row_number){

    let unit_cell = document.getElementById('order_line-' + row_number + '-unit');
    let price_cell = document.getElementById('order_line-' + row_number + '-price');
    let total_price_cell = document.getElementById('order_line-' + row_number + '-order_line_price');

    let selected_goods = service_id_cell.value;
    let url = "https://127.0.0.1:5009/my_app/unit_and_price/" + selected_goods;

    fetch(url).then(function(response) {
        response.json().then(function(data) {
        unit_cell.value = data.unit.unit;
        price_cell.value = data.price.price;
        total_price_cell.value = document.getElementById('order_line-' + row_number + '-quantity').value * price_cell.value;

        get_order_total_price();

        });
    });
}

function recountOrderLinePriceWhenChangingQuantity(quantity_column, row_number) {

    let service_quantity = quantity_column.value;
    let total_price = document.getElementById('order_line-' + row_number + '-order_line_price');
    let service_price = document.getElementById('order_line-' + row_number + '-price').value;

    total_price.value = service_quantity * service_price;

    get_order_total_price();
}


function deleteOrderLine(table_row) {
    let rows_quantity = document.getElementById("order-lines").rows.length;
    if (rows_quantity > 1) {
        table_row.remove();
        get_order_total_price();
     } else {
        alert('There must be minimum one row in the order');
    }
}

const pathname = window.location.pathname;
if (pathname.includes('add_order') || pathname.includes('edit_order')){

    //recount order total price
    get_order_total_price()

    // handler for adding new order line
    const element = document.getElementById("add-line");
    element.addEventListener("click", addRow);

    // handler for recounting order line price when change service or quantity
    document.getElementById("orderTable").addEventListener("input", (e) => {
        let event_id = e.target.attributes['id'];
        let splited_id = event_id.value.split('-');
        let row_number = splited_id[1];
        let column = splited_id[2];

        if (column == "quantity"){ recountOrderLinePriceWhenChangingQuantity(e.target, row_number); }
        else if (column == "service_id"){ recountOrderLinePriceWhenChangingService(e.target, row_number); }

    });

    // handler for deleting order_line
    document.getElementById("orderTable").addEventListener("click", (e) => {
        let event = e.target;
        if (event.matches("#remove-order-line-enabled")) {
            deleteOrderLine(event.closest("tr"))};
    });

}



