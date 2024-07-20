let cnt = 0;

const cont = document.getElementById("cont");

function onBoxClick(me) {
  return () => {
    me.previousSibling?.parentNode.removeChild(me.previousSibling);
    me.nextSibling?.parentNode.removeChild(me.nextSibling);
  };
}

function createBox() {
  const box = document.createElement("div");
  box.className = "box";
  box.textContent = cnt++;
  box.onclick = onBoxClick(box);
  return box;
}

function myOnClick() {
  cont.appendChild(createBox());
}

function myOnClick2() {
  if (cont.lastChild) {
    cont.removeChild(cont.lastChild);
  }
}