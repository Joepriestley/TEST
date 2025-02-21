
        let home={
            lat:30.57,
            long:-9.07,
            zoom:10
        };
        
        let parcellesLayer;  // letiable pour stocker la couche GeoJSON complète
        let allData;  // Stocker toutes les données pour filtrer sans recharger


        let map = L.map('map').setView([30.57,-9.07],9);// Centré sur Maroc

        
       // L.control.browserPrint({position: 'topleft'}).addTo(map);
    

         //L.tileLayer('http://{s}.google.com/vt?lyrs=m&x={x}&y={y}&z={z}',{
           // maxZoom: 20,
           // subdomains:['mt0','mt1','mt2','mt3']
        //})

        let googleHybrid = L.tileLayer('http://{s}.google.com/vt?lyrs=s,h&x={x}&y={y}&z={z}',{
            maxZoom: 20,
            subdomains:['mt0','mt1','mt2','mt3']
        })

        let googleSat = L.tileLayer('http://{s}.google.com/vt?lyrs=s&x={x}&y={y}&z={z}',{
            maxZoom: 20,
            subdomains:['mt0','mt1','mt2','mt3']
        }).addTo(map);

        let googleTerrain = L.tileLayer('http://{s}.google.com/vt?lyrs=p&x={x}&y={y}&z={z}',{
            maxZoom: 20,
            subdomains:['mt0','mt1','mt2','mt3'] 
        })//.addTo(map);

        let googleStreets =L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        })//.addTo(map);
      
        //let imageLnik = staticUrl + "openstreet.JPG";
        let staticUrl = document.getElementById("static-container").getAttribute("data-static-url");
        
        let baseLayers = {
            [`<div class='layer-option'><img title='Google Street Map' src='${staticUrl}sigweb/image/openstreet.JPG' class='layer-icon'/></div>`]: googleStreets,
            [`<div class='layer-option'><img title='Google Hybrid Map' src='${staticUrl}sigweb/image/hybrid.JPG' class='layer-icon'/></div>`]: googleHybrid,
            [`<div class='layer-option'><img title='Google Satellite Map' src='${staticUrl}sigweb/image/sat.JPG' class='layer-icon'/></div>`]: googleSat,
            [`<div class='layer-option'><img title='Google Terrain Map' src='${staticUrl}sigweb/image/terr.JPG' class='layer-icon'/></div>`]: googleTerrain,
    
        };
        

        let overLays={
           // "Parcell":parcellesLayer,
        }
        

        L.control.layers(baseLayers, overLays,{collapsed:false}).addTo(map);


        // Charger les données depuis l'API
        fetch('/Parcelle/')
            .then(response => response.json())
            .then(data => {
                allData = data;  // Stocker les données d'origine
                afficherParcelles(data);  // Afficher toutes les parcelles initialement
                remplirMenusDeroulants(data);  // Remplir les menus déroulants
                afficherListeParcelles(data);  // Afficher la liste des parcelles
            })
            .catch(error => console.error('Erreur de chargement des données:', error));

        // Fonction pour afficher les parcelles sur la carte
        function afficherParcelles(data) {
            if (parcellesLayer) {
                map.removeLayer(parcellesLayer); // Supprimer l'ancienne couche avant de recharger
            }

            parcellesLayer = L.geoJSON(data, {
                onEachFeature: function (feature, layer) {
                    if (feature.properties) {
                        let popupContent = `
                            <b>Numéro dossier :</b> ${feature.properties.num_dossie} <br>
                            <b>Province :</b> ${feature.properties.province} <br>
                            <b>Commune :</b> ${feature.properties.commune} <br>
                            <b>Douar :</b> ${feature.properties.douar} <br>
                            <b>Cercle :</b> ${feature.properties.cercle} <br>
                            <b>Status :</b> ${feature.properties.status} <br>
                            <b>Consistance :</b> ${feature.properties.consistanc} <br>
                            <b>Nombre de façade :</b> ${feature.properties.nb_de_faca} <br>
                            <b>DWG :</b> <a href="${feature.properties.fchier_dwg}">Cliquez ici</a><br>
                            <b>PDF :</b> <a href="${feature.properties.fchier_pdf}">Cliquez ici</a>
                        `;
                        layer.bindPopup(popupContent);
                    }
                }
            }).addTo(map);

            // Zoomer sur les résultats avec un style personnalisé
            let bounds = parcellesLayer.getBounds();
            if (bounds.isValid()) {
                map.fitBounds(bounds, {
                    padding: [50, 50],  // Ajouter du padding pour ne pas coller les bords
                    maxZoom: 16,  // Limiter le zoom maximum
                    animate: true,  // Activer l'animation
                    duration: 2  // Durée de l'animation en secondes
                });
            }
        }

        // Remplir les menus déroulants avec les données de GeoJSON
        function remplirMenusDeroulants(data) {
            let numParcelleSelect = document.getElementById("numParcelle");
            let consistanceSelect = document.getElementById("consistance");
            let communeSelect = document.getElementById("commune");
            let provinceSelect = document.getElementById("province");
            let douarselect = document.getElementById("douar");
            let cercleSelect = document.getElementById("cercle");
            let statusSelect = document.getElementById("status");
            
            

            // Remplir le menu déroulant du numéro de parcelle
            let parcelleSet = new Set();
            let consistanceSet = new Set();
            let communeSet = new Set();
            let provinceSet = new Set();
            let douarSet = new Set();
            let cercleSet = new Set();
            let statusSet = new Set();
          

            data.features.forEach(feature => {
                parcelleSet.add(feature.properties.num_parcel);
                consistanceSet.add(feature.properties.consistanc);
                communeSet.add(feature.properties.commune);

                provinceSet.add(feature.properties.province);
                douarSet.add(feature.properties.douar);
                cercleSet.add(feature.properties.cercle);
                statusSet.add(feature.properties.status);
                
            });

            parcelleSet.forEach(num => {
                let option = document.createElement("option");
                option.value = num;
                option.textContent = num;
                numParcelleSelect.appendChild(option);
            });

            consistanceSet.forEach(cons => {
                let option = document.createElement("option");
                option.value = cons;
                option.textContent = cons;
                consistanceSelect.appendChild(option);
            });
            communeSet.forEach(cons => {
                let option = document.createElement("option");
                option.value = cons;
                option.textContent = cons;
                communeSelect.appendChild(option);
            });

            provinceSet.forEach(cons => {
                let option = document.createElement("option");
                option.value = cons;
                option.textContent = cons;
                provinceSelect.appendChild(option);
            });

            douarSet.forEach(cons => {
                let option = document.createElement("option");
                option.value = cons;
                option.textContent = cons;
                douarselect.appendChild(option);
            });

            cercleSet.forEach(cons => {
                let option = document.createElement("option");
                option.value = cons;
                option.textContent = cons;
                cercleSelect.appendChild(option);
            });

            statusSet.forEach(cons => {
                let option = document.createElement("option");
                option.value = cons;
                option.textContent = cons;
                statusSelect.appendChild(option);
            });

           
        }

        // Fonction pour afficher la liste des parcelles
        function afficherListeParcelles(data) {
            let parcellesList = document.getElementById("parcellesList");
            parcellesList.innerHTML = "";  // Vider la liste avant de la remplir

            data.features.forEach(feature => {
                let li = document.createElement("li");
                li.textContent = `Numéro de Parcelle: ${feature.properties.num_parcel}`;
                li.style.cursor = "pointer";  // Indiquer que l'élément est cliquable

                // Ajouter un gestionnaire d'événements pour zoomer sur la parcelle lorsqu'elle est cliquée
                li.onclick = function() {
                    let bounds = L.geoJSON(feature).getBounds();
                    map.fitBounds(bounds, {
                        padding: [50, 50],  // Ajouter du padding pour ne pas coller les bords
                        maxZoom: 16,  // Limiter le zoom maximum
                        animate: true,  // Activer l'animation
                        duration: 2  // Durée de l'animation en secondes
                    });
                };

                parcellesList.appendChild(li);
            });
        }

        // Fonction pour filtrer les parcelles
        function filtrerParcelles() {
            let numParcelle = document.getElementById("numParcelle").value;
            let consistance = document.getElementById("consistance").value;
            let commune = document.getElementById("commune").value;

            let province = document.getElementById("province").value;
            let douar = document.getElementById("douar").value;
            let cercle = document.getElementById("cercle").value;
            let status = document.getElementById("status").value;
            

            // Filtrer les données GeoJSON
            let filteredData = {
                type: "FeatureCollection",
                features: allData.features.filter(feature => {
                    let matchNumParcelle = numParcelle === "" || feature.properties.num_parcel === numParcelle;
                    let matchConsistance = consistance === "" || feature.properties.consistanc === consistance;
                    let matchcommune = commune === "" || feature.properties.commune === commune;
                    let matchcprovince = province === "" || feature.properties.province === province;
                    let matchdouar = douar === "" || feature.properties.douar === douar;
                    let matchcercle = cercle === "" || feature.properties.cercle === cercle;
                    let matchstatus = status === "" || feature.properties.status === status;
                   

                    return matchNumParcelle && matchConsistance && matchcommune&& matchcprovince && matchdouar && matchcercle && matchstatus  ;
                })
            };

            afficherParcelles(filteredData);
            afficherListeParcelles(filteredData);  // Mettre à jour la liste des parcelles filtrées
        }

        // Fonction pour afficher/cacher le menu
        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('open');
        }

        // Fermer le menu en cliquant en dehors
        document.addEventListener('click', function(event) {
            const sidebar = document.getElementById('sidebar');
            const button = document.querySelector('.toggle-btn');
            if (!sidebar.contains(event.target) && !button.contains(event.target)) {
                sidebar.classList.remove('open');
            }
        });
        //Mouse position coordinates
        $(document).ready(function () {
            map.on("mousemove", function (m) {
                if (m.latlng) {
                    $("#coordinates").html(`${m.latlng.lat.toFixed(7)} ; ${m.latlng.lng.toFixed(7)}`);
                }
            });
        });
// CONTROLS 
        //home button
        L.easyButton('<i class="fa fa-home fa-lg" title="Zoom to home"></i>',(btn,map)=>{
            map.setView([home.lat, home.long],home.zoom);
            $(window).on("resize",()=>{
                $("#map").height($(window));
                map.invalidateSize();
            }).trigger("resize");
        },'Zoom To Home').addTo(map);

        //scalebar 
        L.control.scale({
            position:"bottomright"
        }).addTo(map)

        //zoomControl Position 
        map.zoomControl.setPosition("bottomright");
        let ctrP = L.control.pan({position:"topright"}).addTo(map);
        //Mesure de distance et direction
        let mapRuler = L.control.ruler().addTo(map);

        // Fullscreen control
        map.addControl(new L.Control.FullScreen({
            position:"topright"
           
        }));

        
       

