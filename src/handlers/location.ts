import { Request, Response } from "express";

// Dummy producer
const producer: any = {}
// Dummy protoc generated code
const VehicleLocationEvent: any = {}

export default class TutorialController {
  async create(req: Request, res: Response) {
    try {
      res.status(201).json({
        message: "create OK",
        reqBody: req.body
      });
    } catch (err) {
      res.status(500).json({
        message: "Internal Server Error!"
      });
    }
  }

  async findAll(req: Request, res: Response) {
    try {
      res.status(200).json({
        message: "findAll OK"
      });
    } catch (err) {
      res.status(500).json({
        message: "Internal Server Error!"
      });
    }
  }

  async findOne(req: Request, res: Response) {
    try {
      res.status(200).json({
        message: "findOne OK",
        reqParamId: req.params.id
      });
    } catch (err) {
      res.status(500).json({
        message: "Internal Server Error!"
      });
    }
  }

  async update(req: Request, res: Response) {
    try {
      // Check that latitude and longitude were included in request
      if(!req.body.latitude || !req.body.longitude) {
        res.status(400).json({
          message: "Missing latitude and longitude",
        });
      }

      // Create event using protoc generated type
      const locationEvent = VehicleLocationEvent.create({
        agencyId: req.body.agencyId,
        vehicleId: req.body.vehicleId,
        routeId: req.body.routeId,
        latitude: req.body.latitude,
        longitude: req.body.longitude,
        occupancyLevel: req.body.occupancyLevel,
        timestamp: new Date(),
      })
      
      // Send to Kafka
      await producer.send({
        topic: 'vehicle-location-events',
        messages: [
          locationEvent,
        ],
      })
      
      res.status(200).json({
        message: "Success",
      });
    } catch (err) {
      res.status(500).json({
        message: "Internal Server Error!"
      });
    }
  }

  async delete(req: Request, res: Response) {
    try {
      res.status(200).json({
        message: "delete OK",
        reqParamId: req.params.id
      });
    } catch (err) {
      res.status(500).json({
        message: "Internal Server Error!"
      });
    }
  }
}
