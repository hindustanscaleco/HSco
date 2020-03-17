

const numbers = [34,5,56,56,67]

let sum = 0;    
for (let x of numbers)
    sum += x;

console.log(sum)

const thes = numbers.reduce(
    (accumulator, currentValue) => accumulator + currentValue
    );

console.log(thes)