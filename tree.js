//done by julien zamor

var matriarch = {"name":"Amélie", "age": 104, "sex": "f", "parent":null}

var tree = [
    {"name":"Jack", "age": 86, "sex": "m", "parent":"Amélie"},
    {"name":"Roseline", "age": 79, "sex": "f", "parent":"Amélie"},
    {"name":"Olivier", "age": 59, "sex": "m", "parent":"Jack"},
    {"name":"Pascal", "age": 59, "sex": "m", "parent":"Jack"},
    {"name":"Angélique", "age": 18, "sex": "f", "parent":"Olivier"},
    {"name":"Charlotte", "age": 22, "sex": "f", "parent":"Olivier"},
    {"name":"Lucien", "age": 5, "sex": "m", "parent":"Olivier"},
    {"name":"Julien", "age": 33, "sex": "f", "parent":"Pascal"},
    {"name":"Caroline", "age": 30, "sex": "f", "parent":"Pascal"},
];

function Person(data){
    this.name = data.name;
    this.age = data.age;
    this.sex = data.sex;
    this.parent = null;
    this.children = [];
}
function Tree(rootData){
    this._root = new Person(rootData);

    Tree.prototype.traverse = function(callback){

        (function recursive(currentNode){
            for(var i = 0; i < currentNode.children.length; i++){
                recursive(currentNode.children[i]);
            }
            callback(currentNode);
        })(this._root)
    }

    Tree.prototype.add = function(data){
        var child = new Person(data),
            parentName = data.parent,
            parent = null;
        this.traverse(function(person){
            if(person.name === parentName){
                parent = person;
            }
        })
        parent.children.push(child);
        child.parent = parent;
    }
}

var zamor = new Tree(matriarch);

for(p in tree){
    var person = tree[p];
    zamor.add(person);
}

zamor.traverse(function(person){
    console.log(person.name, person.age)
})

function find_younger(family){
    var younger = zamor._root;
    zamor.traverse(function(person){
        if(person.age < younger.age){
            younger = person;
        }
    });
    return younger;
}
var younger = find_younger(zamor)
console.log("Younger :", younger.name, younger.age);

function count(family, predicate){
    var counter = 0;
    family.traverse(function(person){
        counter += predicate(person);
    });
    return counter;
}

function count_women(family){
    return count(family, function(personne){
        return personne.sex == "f" ? 1 : 0;
    })
}
console.log("Nb femmes :", count_women(zamor));

function count_most_child(family){
    var mostChild = {}
    var mostChildNumber = 0

    family.traverse(function(person){
        if(person.children.length > mostChildNumber){
            mostChildNumber = person.children.length;
            mostChild = person;
        }
    })
    return mostChild
}
var mostChild = count_most_child(zamor)
console.log("Le plus d'enfants :", mostChild.name);