let contestElement = document.querySelectorAll("#contests .row");
let faqElement = document.querySelectorAll("#faq ul");

var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};

getJSON("./assets/faq.JSON", (err, data)=>{
    let faqFile = data.entries;
    let len = faqFile.length;

    for (let i = 0; i < len; i++) {
        let li = document.createElement("li");
        let button = document.createElement("button");

        button.setAttribute("data-toggle", "collapse");
        button.setAttribute("data-target", "#faq-" + i);
        button.innerText = faqFile[i].Q;

        let div = document.createElement("div");
        div.classList.add("collapse");
        div.setAttribute("id", "faq-" + i);
        
        faqFile[i].A.forEach(paragraph => {
            div.appendChild(document.createElement("br"));

            let p = document.createElement("p");
            p.innerHTML = paragraph;
            div.appendChild(p);
        });

        li.appendChild(button);
        li.appendChild(div);

        if (i < len/2) {
            faqElement[0].appendChild(li);
        } else {
            faqElement[1].appendChild(li);
        }
    }
});

getJSON("./assets/contests.JSON", (err, data)=>{
    let upcoming = data.upcoming;
    let past = data.past;

    upcoming.forEach(contest => {
        addContest(contest, upcoming, 0);
    });

    past.forEach(contest => {
        addContest(contest, past, 1);
    });
});

function addContest(contest, list, num) {
    let container = document.createElement("div");
    container.setAttribute("class", "col-12 col-sm-6 col-lg-4 p-3");

    let card = document.createElement("div");
    card.classList.add("card");
    
    let img = document.createElement("img");
    img.setAttribute("src", contest.img);
    img.setAttribute("alt", "technology background");
    img.classList.add("card-img-top");

    let cardBody = document.createElement("div");
    cardBody.classList.add("card-body");

    let h5 = document.createElement("h5");
    h5.classList.add("card-title");
    h5.innerText = contest.title;

    let p = document.createElement("p");
    p.classList.add("card-text");
    p.innerText = contest.date;

    let a = document.createElement("a");
    a.classList.add("btn");
    a.setAttribute("data-mdb-ripple-color", "light");
    a.setAttribute("type", "button");
    a.setAttribute("href", contest.url);
    a.setAttribute("target", "_blank");
    a.innerText = "View Contest";

    cardBody.appendChild(h5);
    cardBody.appendChild(p);
    if (contest.url !== "") {
        cardBody.appendChild(a);
    }
    card.appendChild(img);
    card.appendChild(cardBody);
    container.appendChild(card);
    contestElement[num].appendChild(container);
}