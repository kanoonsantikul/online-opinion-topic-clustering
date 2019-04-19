var clusters = [];

var dataSelection = document.getElementById('dataSelection');
var algorithmSelection = document.getElementById('algorithmSelection');
var clusterSelection = document.getElementById('clusterSelection');
var commentsDiv = document.getElementById('comments');

function startApp (algorithm) {
    for (i = 0; i < algorithmSelection.options.length; i++) {
        if (algorithmSelection.options[i].value === algorithm) {
            algorithmSelection.options[i].setAttribute('selected', 'selected');
        }    
    }

    algorithmSelection.onchange = function () {
        window.location = '/?algorithm=' + algorithmSelection.value;
    }

    for (i = 0; i < dataSelection.children.length; i++) {
        var url = '/?algorithm=' + algorithmSelection.value + '&data=' + dataSelection.children[i].getAttribute('value');
        dataSelection.children[i].setAttribute('href', url);
    }
}

function showData (jsonString) {
    var corpus = JSON.parse(jsonString);
    var corpusLen = Object.keys(corpus.comment).length;

    for (i = 0; i < corpusLen; i++) {
        var predictedLabel = corpus.predicted_label[i];
        if (typeof clusters[predictedLabel] == 'undefined') {
            clusters[predictedLabel] = [];
        } else {
            clusters[predictedLabel].push(corpus.comment[i]);
        }
    }

    addButtons();
}

function addButtons () {
    for (i = 0; i < clusters.length; i++) {
        var a = document.createElement('a');
        a.setAttribute('value', i);
        a.setAttribute('href', '#');
        a.appendChild(document.createTextNode('Cluster ' + i));
        a.onclick = function () {
            while (commentsDiv.firstChild) {
                commentsDiv.removeChild(commentsDiv.firstChild);
            }
            
            var clusterNum = this.getAttribute('value');
            for (i = 0; i < clusters[clusterNum].length; i++) {
                console.log(clusterNum);
                var comment = document.createElement('tr');
                comment.appendChild(document.createTextNode(clusters[clusterNum][i]));
                commentsDiv.appendChild(comment);
            }

            return false;
        }
        clusterSelection.appendChild(a);
    }
}