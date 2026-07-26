
      (function () {
        "use strict";
        var REQUIRED = ["id", "payment_id", "requested_execution_date", "payment_amount",
          "currency", "debtor_name", "debtor_account_IBAN", "debtor_agent_BIC",
          "creditor_name", "creditor_account_IBAN", "creditor_agent_BIC"];
        var BIC_RE = /^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$/;
        var DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
        var AMOUNT_RE = /^\d+(\.\d{1,2})?$/;
        var CCY_RE = /^[A-Z]{3}$/;

        function ibanValid(iban) {
          var s = iban.replace(/\s+/g, "").toUpperCase();
          if (!/^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$/.test(s)) return false;
          var r = s.slice(4) + s.slice(0, 4);
          var expanded = "";
          for (var i = 0; i < r.length; i++) {
            var c = r.charCodeAt(i);
            expanded += (c >= 65) ? String(c - 55) : r[i];
          }
          var mod = 0;
          for (var j = 0; j < expanded.length; j += 7) {
            mod = parseInt(String(mod) + expanded.slice(j, j + 7), 10) % 97;
          }
          return mod === 1;
        }

        function parseCsv(text) {
          var lines = text.trim().split(/\r?\n/).filter(function (l) { return l.trim(); });
          if (lines.length < 2) return { error: "Need a header row and at least one record." };
          var head = lines[0].split(",").map(function (h) { return h.trim(); });
          var rows = lines.slice(1).map(function (line) {
            var cells = line.split(",");
            var rec = {};
            head.forEach(function (h, i) { rec[h] = (cells[i] || "").trim(); });
            return rec;
          });
          return { head: head, rows: rows };
        }

        function validate(rows) {
          var errors = [];
          rows.forEach(function (rec, idx) {
            var row = "row " + (idx + 1);
            REQUIRED.forEach(function (f) {
              if (!rec[f]) errors.push(row + ": missing required field ‘" + f + "’");
            });
            if (rec.payment_amount && !AMOUNT_RE.test(rec.payment_amount)) {
              errors.push(row + ": payment_amount ‘" + rec.payment_amount + "’ is not a valid decimal amount");
            }
            if (rec.currency && !CCY_RE.test(rec.currency)) {
              errors.push(row + ": currency ‘" + rec.currency + "’ is not a 3-letter ISO 4217 code");
            }
            if (rec.requested_execution_date && !DATE_RE.test(rec.requested_execution_date)) {
              errors.push(row + ": requested_execution_date must be YYYY-MM-DD");
            }
            ["debtor_account_IBAN", "creditor_account_IBAN"].forEach(function (f) {
              if (rec[f] && !ibanValid(rec[f])) {
                errors.push(row + ": " + f + " ‘" + rec[f] + "’ fails the ISO 13616 mod-97 checksum");
              }
            });
            ["debtor_agent_BIC", "creditor_agent_BIC"].forEach(function (f) {
              if (rec[f] && !BIC_RE.test(rec[f].toUpperCase())) {
                errors.push(row + ": " + f + " ‘" + rec[f] + "’ is not a valid ISO 9362 BIC");
              }
            });
          });
          return errors;
        }

        function esc(v) {
          return String(v).replace(/&/g, "&amp;").replace(/</g, "&lt;")
            .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
        }

        function toXml(rows) {
          var cents = rows.reduce(function (sum, r) {
            var parts = r.payment_amount.split(".");
            return sum + parseInt(parts[0], 10) * 100 + (parts[1] ? parseInt((parts[1] + "0").slice(0, 2), 10) : 0);
          }, 0);
          var ctrl = Math.floor(cents / 100) + "." + String(cents % 100).padStart(2, "0");
          var msgId = "DEMO-" + Date.now();
          var first = rows[0];
          var tx = rows.map(function (r) {
            return [
              "      <CdtTrfTxInf>",
              "        <PmtId><EndToEndId>" + esc(r.payment_id) + "</EndToEndId></PmtId>",
              "        <Amt><InstdAmt Ccy=\"" + esc(r.currency) + "\">" + esc(r.payment_amount) + "</InstdAmt></Amt>",
              "        <CdtrAgt><FinInstnId><BICFI>" + esc(r.creditor_agent_BIC) + "</BICFI></FinInstnId></CdtrAgt>",
              "        <Cdtr><Nm>" + esc(r.creditor_name) + "</Nm></Cdtr>",
              "        <CdtrAcct><Id><IBAN>" + esc(r.creditor_account_IBAN) + "</IBAN></Id></CdtrAcct>",
              r.remittance_information ? "        <RmtInf><Ustrd>" + esc(r.remittance_information) + "</Ustrd></RmtInf>" : null,
              "      </CdtTrfTxInf>"
            ].filter(Boolean).join("\n");
          }).join("\n");
          return ['<?xml version="1.0" encoding="UTF-8"?>',
            '<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.09">',
            "  <CstmrCdtTrfInitn>",
            "    <GrpHdr>",
            "      <MsgId>" + msgId + "</MsgId>",
            "      <CreDtTm>" + new Date().toISOString().slice(0, 19) + "</CreDtTm>",
            "      <NbOfTxs>" + rows.length + "</NbOfTxs>",
            "      <CtrlSum>" + ctrl + "</CtrlSum>",
            "      <InitgPty><Nm>" + esc(first.debtor_name) + "</Nm></InitgPty>",
            "    </GrpHdr>",
            "    <PmtInf>",
            "      <PmtInfId>" + esc(first.id) + "</PmtInfId>",
            "      <PmtMtd>TRF</PmtMtd>",
            "      <NbOfTxs>" + rows.length + "</NbOfTxs>",
            "      <CtrlSum>" + ctrl + "</CtrlSum>",
            "      <ReqdExctnDt><Dt>" + esc(first.requested_execution_date) + "</Dt></ReqdExctnDt>",
            "      <Dbtr><Nm>" + esc(first.debtor_name) + "</Nm></Dbtr>",
            "      <DbtrAcct><Id><IBAN>" + esc(first.debtor_account_IBAN) + "</IBAN></Id></DbtrAcct>",
            "      <DbtrAgt><FinInstnId><BICFI>" + esc(first.debtor_agent_BIC) + "</BICFI></FinInstnId></DbtrAgt>",
            tx,
            "    </PmtInf>",
            "  </CstmrCdtTrfInitn>",
            "</Document>"].join("\n");
        }

        var SAMPLE = "id,payment_id,requested_execution_date,payment_amount,currency,debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name,creditor_account_IBAN,creditor_agent_BIC,remittance_information\n" +
          "1,TXN-001,2026-08-03,1250.00,EUR,Acme Global Corp,DE89370400440532013000,DEUTDEFFXXX,Supplier SARL,FR1420041010050500013M02606,BNPAFRPPXXX,INVOICE-2026-4411\n" +
          "2,TXN-002,2026-08-03,890.50,EUR,Acme Global Corp,DE89370400440532013000,DEUTDEFFXXX,Northwind Ltd,GB29NWBK60161331926819,NWBKGB2LXXX,INVOICE-2026-4412";

        var input = document.getElementById("csv-input");
        var status = document.getElementById("status");
        var errList = document.getElementById("errors");
        var xmlOut = document.getElementById("xml-out");
        var copyBtn = document.getElementById("copy-btn");
        var downloadBtn = document.getElementById("download-btn");
        var editorBlock = document.getElementById("editor-block");
        var dropzone = document.getElementById("dropzone");
        var fileInput = document.getElementById("file-input");

        function runValidation() {
          errList.innerHTML = "";
          var parsed = parseCsv(input.value);
          if (parsed.error) {
            status.textContent = "✗ " + parsed.error;
            status.className = "status fail";
            xmlOut.textContent = "—";
            copyBtn.disabled = true;
            downloadBtn.disabled = true;
            return;
          }
          var errors = validate(parsed.rows);
          if (errors.length) {
            status.textContent = "✗ Validation failed — " + errors.length + " issue(s). This file would be rejected.";
            status.className = "status fail";
            errors.slice(0, 12).forEach(function (e) {
              var li = document.createElement("li");
              li.textContent = e;
              errList.appendChild(li);
            });
            xmlOut.textContent = "— no XML generated: validation is a hard gate —";
            copyBtn.disabled = true;
            downloadBtn.disabled = true;
          } else {
            status.textContent = "✓ " + parsed.rows.length + " record(s) valid — control totals recomputed. Exit code 0.";
            status.className = "status pass";
            xmlOut.textContent = toXml(parsed.rows);
            copyBtn.disabled = false;
            downloadBtn.disabled = false;
          }
        }

        function loadData(text) {
          input.value = text.trim();
          editorBlock.hidden = false;
          runValidation();
          status.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "center" });
        }

        function readFile(file) {
          if (!file) return;
          if (file.size > 2 * 1024 * 1024) {
            status.textContent = "✗ File is larger than 2 MB — this demo caps input size; the CLI streams batches of any size.";
            status.className = "status fail";
            return;
          }
          var reader = new FileReader();
          reader.onload = function () { loadData(String(reader.result)); };
          reader.onerror = function () {
            status.textContent = "✗ Could not read that file.";
            status.className = "status fail";
          };
          reader.readAsText(file);
        }

        document.getElementById("browse-btn").addEventListener("click", function () { fileInput.click(); });
        fileInput.addEventListener("change", function () { readFile(fileInput.files[0]); fileInput.value = ""; });
        document.getElementById("sample-btn").addEventListener("click", function () { loadData(SAMPLE); });

        ["dragover", "dragenter"].forEach(function (ev) {
          dropzone.addEventListener(ev, function (e) { e.preventDefault(); dropzone.classList.add("dragover"); });
        });
        ["dragleave", "drop"].forEach(function (ev) {
          dropzone.addEventListener(ev, function (e) { e.preventDefault(); dropzone.classList.remove("dragover"); });
        });
        dropzone.addEventListener("drop", function (e) {
          readFile(e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]);
        });

        document.getElementById("run-btn").addEventListener("click", runValidation);

        document.getElementById("break-btn").addEventListener("click", function () {
          /* Bump the first IBAN's check digit so the mod-97 test fails. */
          var m = input.value.match(/[A-Z]{2}\d{2}[A-Z0-9]{10,30}/);
          if (m) {
            var iban = m[0];
            var flipped = iban.slice(0, 2) + ((parseInt(iban[2], 10) + 1) % 10) + iban.slice(3);
            input.value = input.value.replace(iban, flipped);
            status.textContent = "One IBAN check digit changed — press “Validate & generate” to see it caught.";
            status.className = "status";
          }
        });

        copyBtn.addEventListener("click", function () {
          navigator.clipboard.writeText(xmlOut.textContent).then(function () {
            copyBtn.textContent = "Copied ✓";
            setTimeout(function () { copyBtn.textContent = "Copy XML"; }, 1600);
          });
        });

        downloadBtn.addEventListener("click", function () {
          var blob = new Blob([xmlOut.textContent], { type: "application/xml" });
          var a = document.createElement("a");
          a.href = URL.createObjectURL(blob);
          a.download = "pain001-demo.xml";
          document.body.appendChild(a);
          a.click();
          a.remove();
          URL.revokeObjectURL(a.href);
        });

        /* ==== Step 3: official XSD validation via Pyodide + xmlschema. ==== */
        var xsdBtn = document.getElementById("xsd-btn");
        var xsdStatus = document.getElementById("xsd-status");
        var xsdErrors = document.getElementById("xsd-errors");
        var pyodideReady = null;

        function xmlAvailable() {
          return xmlOut.textContent.indexOf("<?xml") === 0;
        }
        function refreshXsdBtn() { xsdBtn.disabled = !xmlAvailable(); }
        new MutationObserver(refreshXsdBtn).observe(xmlOut, { childList: true, characterData: true, subtree: true });
        refreshXsdBtn();

        function loadEngine() {
          if (pyodideReady) return pyodideReady;
          pyodideReady = new Promise(function (resolve, reject) {
            var s = document.createElement("script");
            s.src = "/pyodide/pyodide.js";
            s.onload = resolve;
            s.onerror = function () { reject(new Error("engine script failed to load")); };
            document.head.appendChild(s);
          }).then(function () {
            xsdStatus.textContent = "Starting Python runtime…";
            return loadPyodide({ indexURL: "/pyodide/" });
          }).then(function (py) {
            xsdStatus.textContent = "Loading xmlschema…";
            return py.loadPackage(["/pyodide/elementpath-5.1.3-py3-none-any.whl",
                                   "/pyodide/xmlschema-4.3.2-py3-none-any.whl"])
              .then(function () { return fetch("/pyodide/pain.001.001.09.xsd"); })
              .then(function (r) { return r.text(); })
              .then(function (xsd) {
                py.FS.writeFile("/pain.001.001.09.xsd", xsd);
                py.runPython("import xmlschema\nschema = xmlschema.XMLSchema('/pain.001.001.09.xsd')");
                return py;
              });
          });
          return pyodideReady;
        }

        xsdBtn.addEventListener("click", function () {
          if (!xmlAvailable()) return;
          xsdErrors.innerHTML = "";
          xsdStatus.className = "status";
          xsdStatus.textContent = "Downloading the engine (~13 MB, first run only)…";
          xsdBtn.disabled = true;
          loadEngine().then(function (py) {
            xsdStatus.textContent = "Validating against the official schema…";
            py.globals.set("xml_text", xmlOut.textContent);
            var result = py.runPython(
              "import json\n" +
              "errs = [str(e.reason or e) for e in schema.iter_errors(xml_text)]\n" +
              "json.dumps(errs[:10])"
            );
            var errs = JSON.parse(result);
            if (errs.length === 0) {
              xsdStatus.className = "status pass";
              xsdStatus.textContent = "✓ Valid against the official ISO 20022 pain.001.001.09 XSD.";
            } else {
              xsdStatus.className = "status fail";
              xsdStatus.textContent = "✗ Official schema rejected the document — " + errs.length + " error(s).";
              errs.forEach(function (e) {
                var li = document.createElement("li");
                li.textContent = e;
                xsdErrors.appendChild(li);
              });
            }
            xsdBtn.disabled = false;
          }).catch(function (err) {
            pyodideReady = null;
            xsdStatus.className = "status fail";
            xsdStatus.textContent = "✗ Engine failed to load: " + err.message + ". Check your connection and try again.";
            xsdBtn.disabled = false;
          });
        });
      })();
    