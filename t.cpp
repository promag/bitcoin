#include <vector>

using namespace std;


class X {
  int x;
public:
  X(int _x) : x(_x) {
    printf("init X with %d\n", x);
  }
  X(const X& rhs) : x(rhs.x) {
    printf("copy X\n");
  }
  X(X&& rhs) : x(rhs.x) {
    printf("move X\n");
  }
};


X foo(int a, int b) {
  return X(a+b);
}

int main() {
  vector<X> xs;

  auto x = foo(1, 2);
  xs.push_back(std::move(x));

  return 0;
}
