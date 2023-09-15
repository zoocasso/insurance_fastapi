const upload_xlsm_btn = document.querySelector("#upload_xlsm_btn");
const upload_xlsm_file = document.querySelector("#upload_xlsm_file");
function click_upload_xlsm_btn(e){
	e.preventDefault()
	
	var formdata = new FormData();
	formdata.append('file', upload_xlsm_file.files[0])

	fetch('http://127.0.0.1:8001/uploadfile/',{
		method:'POST',
		body:formdata,
	})
};
upload_xlsm_btn.addEventListener("click",click_upload_xlsm_btn);



const upload_xlsx_btn = document.querySelector("#upload_xlsx_btn")
const upload_xlsx_file = document.querySelector("#upload_xlsx_file")
function click_upload_xlsx_btn(e){
    e.preventDefault()
    
    var formdata = new FormData();
    formdata.append('file', upload_xlsx_file.files[0])

    fetch('/xlsx_parsing',{
        method:'POST',
        body:formdata,
    })
};
upload_xlsx_btn.addEventListener("click",click_upload_xlsx_btn)