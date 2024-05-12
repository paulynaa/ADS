#include<iostream>
#include<random>
#include<cmath>
#include<ctime>
using namespace std;

int main() {
    int viso_tasku;
    double x, y, atstumas, pi_apyt;
    int taskai_apskritime = 0;

    cout << "Irasykite kiek tasku norite simuliuoti: ";
    cin >> viso_tasku;

    srand(time(NULL));

    for (int i = 0; i < viso_tasku * 10; ++i) {
        x = (double)rand() / RAND_MAX;
        y = (double)rand() / RAND_MAX;
        atstumas = sqrt(x * x + y * y);
        if (atstumas <= 1.0) {
            taskai_apskritime++;
        }
    }

    pi_apyt = 4.0 * taskai_apskritime / (viso_tasku * 10);

    cout << "PI apytiksliai: " << pi_apyt << endl;

    return 0;
}
