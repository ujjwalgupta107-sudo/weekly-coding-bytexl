#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

#define pb push_back
#define fast_io ios_base::sync_with_stdio(0); cin.tie(0);

bool cmp(pair<int,int> a, pair<int,int> b) {
    return a.second < b.second;
}

int main() {
    fast_io;
    int n;
    if(!(cin >> n)) return 0;

    vector<int> st(n), en(n);
    for(int i=0; i<n; i++) cin >> st[i];
    for(int i=0; i<n; i++) cin >> en[i];

    vector<pair<int,int>> v(n);
    for(int i=0; i<n; i++) {
        v[i] = {st[i], en[i]};
    }
    
    sort(v.begin(), v.end(), cmp);
    
    int ans = 0;
    int last = -1;
    
    for(int i=0; i<n; i++) {
        if(v[i].first >= last) {
            ans++;
            last = v[i].second;
        }
    }
    
    cout << ans << "\n";
    return 0;
}