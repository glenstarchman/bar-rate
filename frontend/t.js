

class Base {

  func1() {
    console.log('hello from func1');
    this.func3();
  }
}


class Child extends Base {

  func2() {
    console.log('func2!')
    super.func1();
  }

  func3() {
    console.log('func3');
  }
}

let a = new Child();
a.func2();
