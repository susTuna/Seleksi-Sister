from Evtx.Evtx import Evtx
import json, argparse

def extract_evtx(evtx_file_path):
    try:
        with Evtx(evtx_file_path) as log:
            events = []
            for record in log.records():
                event_data = {
                    'record_id': record.record_num(),
                    'timestamp': record.timestamp(),
                    'xml_data': record.xml()
                }
                events.append(event_data)

                print(f"Record ID: {record.record_num()}")
                print(f"Timestamp: {record.timestamp()}")
                print(f"XML: {record.xml()}")
                print("-" * 50)
            
            return events
    except Exception as e:
        print(f"Error extracting EVTX: {e}")
        return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract events from EVTX file")
    parser.add_argument("--file", "-f", type=str, required=False, help="Path to the file")
    args = parser.parse_args()

    extracted_events = extract_evtx(args.file)

    with open(f'{args.file}_extracted.json', 'w') as f:
        json.dump(extracted_events, f, indent=2, default=str)

    print(f"Extracted {len(extracted_events)} events from EVTX file")