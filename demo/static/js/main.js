var clusters = [];

var dataSelection = document.getElementsByClassName('card-action');
var algorithms = document.getElementsByName('algorithm');
var clusterSelection = document.getElementById('clusterSelection');
var commentsDiv = document.getElementById('comments');

var activeCluster = document.createElement('div');
var algorithm

function startApp (algorithm, data) {
    this.algorithm = algorithm

    for (i = 0; i < algorithms.length; i++) {
        if (algorithms[i].value === algorithm) {
            algorithms[i].setAttribute('checked', 'checked');
        }
        algorithms[i].onclick = function () {
            window.location = '/?algorithm=' + this.value + '&data=' + data;    
        }
    }

    dataList = document.getElementById('data-list')
    for (i = 0; i < dataList.children.length; i++) {
        if (dataList.children[i].getAttribute('value') == data) {
            dataList.children[i].children[0].classList.add('active')
        } else {
            dataList.children[i].children[0].classList.remove('active')
        }
    }

    for (i = 0; i < dataSelection.length; i++) {
        var link = dataSelection[i].children[0];
        var url = '/?algorithm=' + algorithm + '&data=' + link.getAttribute('value');
        link.setAttribute('href', url);
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
        a.setAttribute('href', '#');
        a.className = "waves-effect waves-teal grey-text text-lighten-2";

        if (i == 0 && algorithm != 'k-mean') {
            a.appendChild(document.createTextNode('Noise Cluster (Total ' + clusters[i].length + ')'))
        } else {
            a.appendChild(document.createTextNode('Cluster ' + i + ' (Total ' + clusters[i].length + ')'));
        }

        var li = document.createElement('li');
        li.setAttribute('value', i);
        li.onclick = function () {
            while (commentsDiv.firstChild) {
                commentsDiv.removeChild(commentsDiv.firstChild);
            }
            
            var clusterNum = this.getAttribute('value');
            for (i = 0; i < clusters[clusterNum].length; i++) {
                var comment = document.createElement('div');
                comment.className = "card-panel amber lighten-4 z-depth-0"
                comment.appendChild(document.createTextNode(clusters[clusterNum][i]));
                commentsDiv.appendChild(comment);
            }

            activeCluster.classList.remove('active');
            activeCluster = this;
            this.className = 'active';
            
            return false;
        }
        li.appendChild(a);
        
        clusterSelection.appendChild(li);
    }

    clusterSelection.children[1].click();
}