function click_upload_excel_btn(e){
	e.preventDefault()
	
	var formdata = new FormData();
	formdata.append('file', upload_excel_file.files[0])

	fetch('http://127.0.0.1:8001/uploadfile/',{
		method:'POST',
		body:formdata,
	})
};

const upload_excel_btn = document.querySelector("#upload_excel_btn");
const upload_excel_file = document.querySelector("#upload_excel_file");

upload_excel_btn.addEventListener("click",click_upload_excel_btn);