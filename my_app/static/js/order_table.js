

function get_order_total_price() {

    const nodeList = document.querySelectorAll(".order-line-price");
    let summ = 0;
    for (let i = 0; i < nodeList.length; i++) {
        summ += Number(nodeList[i].valueAsNumber);
    }
    document.getElementById('order-total-price').innerHTML = summ;

}


const pathname = window.location.pathname;
if (pathname.includes('add_order') || pathname.includes('edit_order')){
    get_order_total_price();
 }


function addRow(unit, price, service_id) {

    let table = document.getElementById("order-lines");

    // Create row element
    let row = document.createElement("tr")

    // Create cells
    let c1 = document.createElement("td")
    let c2 = document.createElement("td")
    let c3 = document.createElement("td")
    let c4 = document.createElement("td")
    let c5 = document.createElement("td")
    let c6 = document.createElement("td")
    let c7 = document.createElement("td")

    // Insert data to cells

    let number_rows = table.rows.length
    let stringToSplit = document.getElementById("myTable").rows.item(number_rows).querySelector('[id]').id
    var separator = '-'
    var chosen_id = Number(stringToSplit.split(separator)[1])
    var ids = chosen_id + 1;


    var elem = document.querySelector('#order_line-' + chosen_id + '-service_id')
    var clone1 = elem.cloneNode(true);
    clone1.id = 'order_line-' + ids + '-service_id';
    clone1.name = 'order_line-' + ids + '-service_id';
    clone1.setAttribute("oninput", "getIndex(this.id)");
    clone1.value = service_id;
    c1.appendChild(clone1)

    var elem = document.querySelector('#order_line-' + chosen_id + '-quantity')
    var clone2 = elem.cloneNode();
    clone2.id = 'order_line-' + ids + '-quantity';
    clone2.name = 'order_line-' + ids + '-quantity';
    clone2.value = 1
    clone2.setAttribute("oninput", "changeQuantity(this.id)");
    c2.appendChild(clone2)

    var elem = document.querySelector('#order_line-' + chosen_id + '-unit')
    var clone3 = elem.cloneNode();
    clone3.id = 'order_line-' + ids + '-unit';
    clone3.name = 'order_line-' + ids + '-unit';
    clone3.value = unit;
    c3.appendChild(clone3)

    var elem = document.querySelector('#order_line-' + chosen_id + '-price')
    var clone4 = elem.cloneNode();
    clone4.id = 'order_line-' + ids + '-price';
    clone4.name = 'order_line-' + ids + '-price';
    clone4.value = price;
    c4.appendChild(clone4)

    var elem = document.querySelector('#order_line-' + chosen_id + '-order_line_price')
    var clone5 = elem.cloneNode();
    clone5.id = 'order_line-' + ids + '-order_line_price';
    clone5.name = 'order_line-' + ids + '-order_line_price';
    clone5.setAttribute('class', 'order-line-price');
    clone5.value = clone4.value
    c5.appendChild(clone5)

    var elem = document.querySelector('#order_line-' + chosen_id + '-event_date')
    var clone6 = elem.cloneNode();
    clone6.id = 'order_line-' + ids + '-event_date';
    clone6.name = 'order_line-' + ids + '-event_date';
    clone6.value= new Date().toJSON().slice(0, 10);
    c6.appendChild(clone6)

    clone7 = document.querySelector('#action').cloneNode();
    c7.appendChild(clone7)
    console.log(clone7);

    // Append cells to row
    row.appendChild(c1);
    row.appendChild(c2);
    row.appendChild(c3);
    row.appendChild(c4);
    row.appendChild(c5);
    row.appendChild(c6);
    row.appendChild(c7);

    // Append row to table body
    table.appendChild(row)

    get_order_total_price();


}

function getIndex(x){
    let goods_select = document.getElementById(x);
    const del_goods = x.replace(/service_id/i, '')
    let unit_select = document.getElementById(del_goods + 'unit');
    let price_select = document.getElementById(del_goods + 'price');
    let total_price_select = document.getElementById(del_goods + 'order_line_price');

    let goods = goods_select.value;
    var partial_url = document.querySelector('#url-without-parameter-to-get-unit-and-price-for-order-line');
    const user_url = partial_url.getAttribute('data-url') + goods;
    fetch(user_url).then(function(response) {
        response.json().then(function(data) {
        unit_select.value = data.unit.unit;
        price_select.value = data.price.price;
        total_price_select.value = document.getElementById(del_goods+'quantity').value * price_select.value;

        get_order_total_price();

        });
    });
}

function changeQuantity(x) {
    var quantity = document.getElementById(x).value;
    const del_quantity = x.replace(/quantity/i, '');
    var total_price_select = document.getElementById(del_quantity+'order_line_price');
    var price_select = document.getElementById(del_quantity+'price').value;
    total_price_select.value = quantity * price_select;

    get_order_total_price();

}


function deleteLine(x) {
    let rows_quantity = document.getElementById("order-lines").rows.length;

    if (rows_quantity > 1) {
        var i = x.parentNode.parentNode.rowIndex;
        document.getElementById('myTable').deleteRow(i);

        get_order_total_price();

    } else {
        alert('There must be minimum one row in the order');
    }


}


