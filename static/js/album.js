
    let popup = document.getElementById("containtAddAlbum");
    let closeBtn = document.getElementById("close");
    let addAlbum = document.getElementById("addAlbum");

    addAlbum.addEventListener('click', ()=>{
        popup.style.display = 'block';
    });

    closeBtn.addEventListener('click' ,() => {
        popup.style.display = 'none';
    });
