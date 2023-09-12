function add_column_btn_func(e){
    fetch('/create',{
        method : 'post',
        headers: {
            "Content-Type": "application/json",
        },      
        body: JSON.stringify({name:add_column_name.value})
    })
}
const add_column_name = document.querySelector('#add_column_name')
const add_column_btn = document.querySelector('#add_column_btn')
add_column_btn.addEventListener('click',add_column_btn_func)



function delete_column_btn_func(e){
    fetch('/delete',{
        method : 'post',
        headers: {
            "Content-Type": "application/json",
        },      
        body: JSON.stringify({name:delete_column_name.value})
    })
}
const delete_column_name = document.querySelector('#delete_column_name')
const delete_column_btn = document.querySelector('#delete_column_btn')
delete_column_btn.addEventListener('click',delete_column_btn_func)



function row_insert_btn_func(e){
    const row_form = document.querySelector('#row_form')
    
    fetch('/row_insert',{
        method : 'post',
        headers: {
            "Content-Type": "application/json",
        },      
        body: JSON.stringify({
            date:row_form['date'].value,
            open:row_form['open'].value,
            high:row_form['high'].value,
            low:row_form['low'].value,
            close:row_form['close'].value,
            volume:row_form['volume'].value,
            change:row_form['change'].value
        })
    })
}

const row_insert_btn = document.querySelector('#row_insert_btn')
row_insert_btn.addEventListener('click',row_insert_btn_func)