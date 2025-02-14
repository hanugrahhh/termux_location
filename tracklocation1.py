# -*- coding: utf-8 -*-
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium

# API Key untuk OpenCage Geocode (Ganti dengan API Key milikmu)
API_KEY = "your_key_here"

# Meminta pengguna memasukkan nomor telepon
number = raw_input("Masukkan nomor telepon (dengan kode negara, misal +6281234567890): ")

try:
    # Parsing nomor telepon
    new_number = phonenumbers.parse(number)

    # Validasi apakah nomor telepon valid
    if not phonenumbers.is_valid_number(new_number):
        print "Nomor telepon tidak valid."
    else:
        # Menampilkan lokasi berdasarkan kode negara
        location = geocoder.description_for_number(new_number, "en")
        print "Lokasi:", location

        # Menampilkan nama operator seluler
        service_name = carrier.name_for_number(new_number, "en")
        print "Operator:", service_name

        # Menggunakan OpenCage untuk mendapatkan koordinat
        geo = OpenCageGeocode(API_KEY)
        result = geo.geocode(location)

        if result:
            lat = result[0]['geometry']['lat']
            lng = result[0]['geometry']['lng']
            print "Koordinat:", lat, ",", lng

            # Membuat peta dengan folium
            my_map = folium.Map(location=[lat, lng], zoom_start=9)
            folium.Marker([lat, lng], popup=unicode(location, "utf-8")).add_to(my_map)

            # Menyimpan peta dalam file HTML
            my_map.save("location.html")
            print "Pelacakan lokasi selesai. Cek file 'location.html'."
        else:
            print "Lokasi tidak ditemukan."
except Exception as e:
    print "Terjadi kesalahan:", str(e)