#include <iostream>
#include <vector>
using namespace std;

void merge(vector<int>& masyvas, int kairysis, int vidurys, int desinysis) {
    int n1 = vidurys - kairysis + 1;
    int n2 = desinysis - vidurys;

    vector<int> kairysisMas(masyvas.begin() + kairysis, masyvas.begin() + kairysis + n1);
    vector<int> desinysisMas(masyvas.begin() + vidurys + 1, masyvas.begin() + vidurys + 1 + n2);

    int i = 0, j = 0, k = kairysis;
    while (i < n1 && j < n2) {
        if (kairysisMas[i] <= desinysisMas[j])
            masyvas[k++] = kairysisMas[i++];
        else
            masyvas[k++] = desinysisMas[j++];
    }

    while (i < n1) masyvas[k++] = kairysisMas[i++];
    while (j < n2) masyvas[k++] = desinysisMas[j++];
}

void mergeSort(vector<int>& masyvas, int kairysis, int desinysis) {
    if (kairysis < desinysis) {
        int vidurys = kairysis + (desinysis - kairysis) / 2;
        mergeSort(masyvas, kairysis, vidurys);
        mergeSort(masyvas, vidurys + 1, desinysis);
        merge(masyvas, kairysis, vidurys, desinysis);
    }
}

int main() {
    vector<int> masyvas;

    int dydis;
    cout << "Iveskite elementu skaiciu: ";
    cin >> dydis;

    cout << "Iveskite " << dydis << " skaicius atskirtus tarpais:\n";
    for (int i = 0; i < dydis; i++) {
        int skaicius;
        cin >> skaicius;
        masyvas.push_back(skaicius);
    }

    mergeSort(masyvas, 0, dydis - 1);

    cout << "Surusiuotas masyvas:\n";
    for (int skaicius : masyvas) cout << skaicius << " ";
    cout << endl;

    return 0;
}
