a = [1, -1, -1, -1, -1]
console.log(a)

b = (a.some((e) => {
    return e === 1
})) ? 1 : -1

console.log(b);